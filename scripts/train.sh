export MODEL_NAME="stabilityai/stable-diffusion-xl-base-1.0"
export INSTANCE_DIR="disney_resized_images"
export OUTPUT_DIR="disney_SDXL_lora"
export HUB_MODEL_ID="ZachX/disney_SDXL_lora"

accelerate launch train_dreambooth_lora_sdxl.py \
  --pretrained_model_name_or_path=$MODEL_NAME  \
  --instance_data_dir=$INSTANCE_DIR \
  --output_dir=$OUTPUT_DIR \
  --mixed_precision="fp16" \
  --instance_prompt="a Disney Style photo" \
  --resolution=1024 \
  --train_batch_size=1 \
  --gradient_accumulation_steps=4 \
  --learning_rate=1e-4 \
  --report_to="wandb" \
  --lr_scheduler="constant" \
  --lr_warmup_steps=0 \
  --max_train_steps=500 \
  --validation_prompt="Disney Style, a cat" \
  --validation_epochs=25 \
  --seed="0" \
  --push_to_hub \
  --hub_model_id=$HUB_MODEL_ID \
  --hub_token=$HUB_API_KEY