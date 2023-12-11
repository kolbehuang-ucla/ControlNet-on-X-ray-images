# ControlNet for Generating X-Ray Images

This is the repository for course project of CS245 in UCLA. Thanks to the efforts from Jihong Huang (kolbehuang@ucla.edu), Lily Lin (lilyl3@ucla.edu), Injae Shin (sij814@ucla.edu), Sherly Yaghoubi (sherlyyaghoubi@ucla.edu), Liping Yin (lipyin@ucla.edu).

## Dataset
The dataset we used is from [NIH Chest X-ray dataset](https://nihcc.app.box.com/v/ChestXray-NIHCC). The original dataset contains 112,120 X-ray images with 14 disease labels from 30,805 unique patients. Due to limited computational resources, we utilizes a [subtset](https://www.kaggle.com/datasets/homayoonkhadivi/chest-xray-worldwide-datasets) of 999 images with the same disease labels.

In the directory "Data", we provide the scripts used to perform the data preprocessing. Notice that the final format is somehow different from the [official requirement](https://github.com/lllyasviel/ControlNet/blob/main/docs/train.md#step-1---get-a-dataset), but the content is the same. 

## Model: ControlNet
The model we are using is [Stable Diffusion + ControlNet](https://github.com/lllyasviel/ControlNet/tree/main). We locked the Stable Diffusion parameters from SD v1.5.

## Training
We utilized the training script from [ControlNet-Trainer](https://github.com/diontimmer/ControlNet-Trainer/tree/main). Due to the limited training dataset, we trained our model based on pre-trained controlnet using canny edges([control_sd15_canny.pth](https://huggingface.co/lllyasviel/ControlNet)) so that it only needs to learn the features of X-rays instead of learning from scratch. This strategy might bias our final model due to the pre-trained ControlNet weights, but it is necessary to do so given limited resources.

To allow training from [control_sd15_canny.pth](https://huggingface.co/lllyasviel/ControlNet), we need to add the file under ./Trainer/models so that the training script will use that instead of loading the default initial weights for ControlNet with SD v1.5.

In the directory "Trainer", we provide our version of ControlNet-Trainer. The file  Pre_trained_ControlNet_Trainer.ipynb provides the commands that we use to train the model.
Some necessary parameters:
- sd_version = "1.5"
- batch_size = 2
- gradient_accumulation_steps = 2
- learning_rate = 1e-5
- max_epochs = 50
- sd_locked = True

We trained our model using the V100 GPU on Colab. The time to train 5 epochs was approximately 1 hour.

### Modification over training script
Notice that we made some modifications on the original training script so that it allows to train based on pre-trained weights. In the function `create_controlnet_model` in share.py, we changed the loading method and the checkpoint to load. You could also change there to allow customized pre-trained weights.

## Inference
We did the inferences over the test data both using the unfinetuned model and the model trained on the training data. The inference captions have the same format that we used to train the model. We used 20 steps to make each inference and pick the first result.

In the directory "Inferences", we provide our inference files. The difference was which version of weights to load into ControlNet with canny edges.

## Evaluation
We evaluated our model's performance over test images given naive prompts. The quantitative metrics are [FID score](https://en.wikipedia.org/wiki/Fr%C3%A9chet_inception_distance) and [SSIM score](https://en.wikipedia.org/wiki/Structural_similarity#:~:text=The%20resultant%20SSIM%20index%20is,of%20size%208%C3%978.). 

In the directory "Evaluation", we provide our evaluation files. There is also a visualization script that can visualize the images on analysis for qualitative evaluation if necessary.

## Ablative study
We did ablative studies on our trained model to see which components were contributing to the controlling performances. The experiments include "no prompt", "Alternative prompt", "conflicting prompt", "perfect prompt", and input images with different level of canny edges (details of input images). 

In the directory "Ablative study", we provide our experiment files.

## FAQs
Q: Can one directly run the code after downloading?
A: We did not include the corresponding dataset and pre-trained weights. Also, the paths that we provide in the .ipynb files are from our drive structure. If you want to run the code, change the paths and download the necessary files as instructed above.

Q: How should one run the code to train the model?
A: We made the whole project and run it on Colab, which is also the reason that we utilized [ControlNet-Trainer](https://github.com/diontimmer/ControlNet-Trainer/tree/main) to install the packages and make the environment on Colab.

Q: How can one turn the traning checkpoints into usable weights for inference?
A: Thanks to convert_original_controlnet_to_diffusers.py in diffusers, we could convert the saved .ckpt file in the ./Trainer/output(which is the output folder that one can make to store the final result). Notice that the training script will save a .safetensors file for each checkpoint, but there seems to be some errors to convert it into usable weights for inference.

## Reference
https://github.com/diontimmer/ControlNet-Trainer/tree/main
https://github.com/lllyasviel/ControlNet/tree/main#readme


 