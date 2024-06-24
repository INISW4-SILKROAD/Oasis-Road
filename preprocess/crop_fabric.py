from mmdet.apis import init_detector, inference_detector
from mmdet.core import DatasetEnum
from PIL import Image
import pickle, os

CONFIG_PATH = 'preprocess/detect_model/custom_detection.py'
WEIGHT_PATH = 'preprocess/detect_model/custom_detection.pth'

class FabricCropper:
    def __init__(self):
        if os.path.exists('model.pkl'):
            with open('model.pkl', 'rb') as f:
                self.model = pickle.load(f)
        else:
            self.model = init_detector(CONFIG_PATH, WEIGHT_PATH, DatasetEnum.COCO, device='cuda:0')
            with open('model.pkl', 'wb') as f:
                pickle.dump(self.model, f)
        
    def crop_bbox(self, id_ ,image_path, output_dir, thd):
        predict = inference_detector(self. model, image_path)
        score = [predict[0][i][4] for i in range(len(predict[0]))]
        
        if max(score) >= thd:
            max_position = score.index(max(score))
            
            image = Image.open(image_path)
            
            cropped_image = image.crop(predict[0][max_position][:4])
            
            path = output_dir + str(id_)+'.jpg'
            cropped_image.save(path)
            return path, max(score)
        
        return None, max(score)

if __name__ =='__main__':
    cropper = FabricCropper()