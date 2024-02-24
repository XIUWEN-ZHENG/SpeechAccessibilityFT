#!/bin/bash
usr=xiuwenz2
source /home/${usr}/.bashrc
PYTHON_VIRTUAL_ENVIRONMENT=/home/${usr}/.conda/envs/wav2vec
conda activate ${PYTHON_VIRTUAL_ENVIRONMENT}

FAIRSEQ_ROOT=/home/${usr}/fairseq
RELEASE=2023-10-05
release=1005
labels=chr
work_dir=/home/xiuwenz2/SpeechAcc/fine-tune

model=wav2vec_base_${release}
model_dir=${work_dir}/outputs/${model}
ckpt_path=${model_dir}/checkpoint_best.pt
manifest_dir=${work_dir}/manifest/${RELEASE}
results_path=${work_dir}/res/${model}
            
mkdir -p ${work_dir}/res
mkdir -p ${results_path}

subset=test
python ${work_dir}/utils/infer.py ${manifest_dir} --task audio_finetuning \
--nbest 1 --path ${ckpt_path} --gen-subset ${subset} --results-path ${results_path} \
--w2l-decoder viterbi --lm-weight 2 --word-score -1 --sil-weight 0 --criterion ctc --labels ${labels} --max-tokens 4000000 \
--post-process letter