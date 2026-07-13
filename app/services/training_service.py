import cv2
import joblib
import numpy as np
from flask import current_app


class TrainingService:
    def train_model(self):
        from sklearn.model_selection import train_test_split
        from tensorflow.keras.layers import Conv2D, Dense, Flatten, MaxPooling2D
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.utils import to_categorical

        data_dir = current_app.config["FACE_DATA_DIR"]
        image_size = current_app.config["FACE_IMAGE_SIZE"]
        X, y, label_dict = [], [], {}
        label_id = 0

        for user_path in data_dir.iterdir() if data_dir.exists() else []:
            if not user_path.is_dir():
                continue

            label_dict[user_path.name] = label_id
            for img_path in user_path.iterdir():
                img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue
                img = cv2.resize(img, (image_size, image_size))
                X.append(img)
                y.append(label_id)
            label_id += 1

        if not X:
            raise RuntimeError("No face images found. Register at least one user before training the model.")

        X = np.array(X).reshape(-1, image_size, image_size, 1) / 255.0
        y = to_categorical(np.array(y))
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        model = Sequential([
            Conv2D(32, (3, 3), activation="relu", input_shape=(image_size, image_size, 1)),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation="relu"),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(128, activation="relu"),
            Dense(y.shape[1], activation="softmax"),
        ])

        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
        model.fit(
            X_train,
            y_train,
            epochs=current_app.config["MODEL_EPOCHS"],
            validation_data=(X_test, y_test),
        )

        current_app.config["MODEL_DIR"].mkdir(parents=True, exist_ok=True)
        model.save(str(current_app.config["MODEL_PATH"]))
        joblib.dump(label_dict, current_app.config["LABEL_PATH"])
