import argparse
from pathlib import Path
from typing import List, Dict

import cv2
import numpy as np


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--images-dir', type=Path, required=True, help='Path to the directory containing the images')
    parser.add_argument('--annotations-dir', type=Path, required=True, help='Path to the directory containing the annotations')
    parser.add_argument('--classes-txt', type=Path, required=True, help='Path to the classes.txt file')
    parser.add_argument('--delay', default=5000, type=int, help='Visualization delay in milliseconds')
    args = parser.parse_args()

    assert args.images_dir.exists(), f'Images directory {args.images_dir} does not exist'
    assert args.annotations_dir.exists(), f'Annotations directory {args.annotations_dir} does not exist'
    assert args.classes_txt.exists(), f'Classes file {args.classes_txt} does not exist'

    images: List[Path] = sorted(args.images_dir.iterdir())
    annotations: List[Path] = [args.annotations_dir / f'{image.stem}.txt' for image in images]
    classes: Dict[int, str] = {i: class_name for i, class_name in enumerate(args.classes_txt.read_text().splitlines())}

    for image, annotation in zip(images, annotations):
        image: np.ndarray = cv2.imread(str(image))
        boxes: List[List[float]] = [list(map(float, x.split())) for x in annotation.read_text().splitlines()]

        for (label, x_center, y_center, width, height) in boxes:
            x1, y1 = int((x_center - width / 2) * image.shape[1]), int((y_center - height / 2) * image.shape[0])
            x2, y2 = int((x_center + width / 2) * image.shape[1]), int((y_center + height / 2) * image.shape[0])

            image = cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 3)
            image = cv2.putText(image, classes[label], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        cv2.imshow('Press Q for exit', cv2.resize(image, (0, 0), fx=0.4, fy=0.4))
        key = cv2.waitKey(args.delay) & 0xFF

        if key == ord('q'):
            break

    cv2.destroyAllWindows()
