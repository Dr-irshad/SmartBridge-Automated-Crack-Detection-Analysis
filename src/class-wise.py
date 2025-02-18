import os
import shutil
import glob

# Define the paths
train_images_path = 'train/images/'
train_labels_path = 'train/labels/'
valid_images_path = 'valid/images/'
valid_labels_path = 'valid/labels/'
test_images_path = 'test/images/'
test_labels_path = 'test/labels/'

# Define class names and folder names
class_names = ['Bullet_imapct', 'Explosion_Impact', 'normal_crack', 'severe_crack']

# Define output directories
output_dirs = {class_name: os.path.join('class_wise', class_name) for class_name in class_names}

# Create directories for each class
for dir in output_dirs.values():
    os.makedirs(dir, exist_ok=True)

def move_images_and_labels(images_path, labels_path):
    # Get all image and label files
    image_files = glob.glob(os.path.join(images_path, '*.jpg'))
    label_files = glob.glob(os.path.join(labels_path, '*.txt'))

    # Ensure each image has a corresponding label
    for image_file in image_files:
        # Get the base filename without extension
        base_name = os.path.basename(image_file).replace('.jpg', '')
        label_file = os.path.join(labels_path, base_name + '.txt')

        if not os.path.exists(label_file):
            continue

        # Read the label file
        with open(label_file, 'r') as f:
            lines = f.readlines()

        # Determine the class and move the image and label
        for line in lines:
            parts = line.strip().split()
            class_id = int(parts[0])
            if class_id < len(class_names):
                class_name = class_names[class_id]
                dest_image_dir = os.path.join(output_dirs[class_name], 'images')
                dest_label_dir = os.path.join(output_dirs[class_name], 'labels')

                # Create class directories if they don't exist
                os.makedirs(dest_image_dir, exist_ok=True)
                os.makedirs(dest_label_dir, exist_ok=True)

                # Move the image and label files
                shutil.copy(image_file, dest_image_dir)
                shutil.copy(label_file, dest_label_dir)
                break

# Process train, validation, and test datasets
move_images_and_labels(train_images_path, train_labels_path)
move_images_and_labels(valid_images_path, valid_labels_path)
move_images_and_labels(test_images_path, test_labels_path)
