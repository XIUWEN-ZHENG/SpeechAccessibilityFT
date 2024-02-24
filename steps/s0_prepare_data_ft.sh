#!/bin/bash

## activate environment
usr=xiuwenz2
source /home/${usr}/.bashrc
PYTHON_VIRTUAL_ENVIRONMENT=/home/${usr}/.conda/envs/wav2vec
conda activate ${PYTHON_VIRTUAL_ENVIRONMENT}

## set stages
stage=0
stop_stage=0

## basic info
task=fine-tune
release=2023-10-05

ext=wav
lang=en
splits="train dev test"
database=/home/xiuwenz2/datasets/SpeechAcc/${release}
datadest=/home/xiuwenz2/SpeechAcc/data/${release}
working_dir=/home/xiuwenz2/SpeechAcc/${task}
manifest_dir=${working_dir}/manifest/${release}

## run stage 0
if [ $stage -le 0 ] && [ $stop_stage -ge 0 ]; then
    echo "Stage 0: resample audios to 16k..."
    mkdir -p ${datadest}
    for split in ${splits}; do
        mkdir -p ${datadest}/${split}
        echo "writing ${release}-${split}-16k to ${datadest}"
        python ${working_dir}/utils/resample.py \
            --tag ${split} \
            --release ${release} \
            --database ${database} \
            --datadest ${datadest} \
            --sr 16000
    done
fi

## run stage 1
if [ $stage -le 1 ] && [ $stop_stage -ge 1 ]; then
    echo "Stage 1: Generate .tsv manifest..."
    mkdir -p ${manifest_dir}
    for split in ${splits}; do
        echo "writing ${release}-${split}.tsv to ${manifest_dir}"
        python ${working_dir}/utils/gen_tsv.py \
            --tag ${split} \
            --datadest ${datadest} \
            --manifest-dir ${manifest_dir}
    done
fi

## run stage 2
if [ $stage -le 2 ] && [ $stop_stage -ge 2 ]; then
    echo "Stage 2: Generate .wrd label..."
    echo "writing all.json to ${datadest}/doc"
    mkdir -p ${datadest}/doc
    python ${working_dir}/utils/gen_json.py \
            --tag test \
            --release ${release} \
            --database ${database} \
            --datadest ${datadest}

    for split in ${splits}; do
        echo "writing ${split}.origin.wrd to ${manifest_dir}"
        python ${working_dir}/utils/gen_wrd.py \
                --tag ${split} \
                --database ${database} \
                --datadest ${datadest} \
                --manifest-dir ${manifest_dir}
    done
    
    for split in ${splits}; do
        echo "writing ${split}.wrd to ${manifest_dir}"
        echo "prerequisite: install nemo_text_processing"
        python ${working_dir}/utils/norm_txt.py \
                --tag ${split} \
                --manifest-dir ${manifest_dir}
    done    
fi
    
## run stage 3
if [ $stage -le 3 ] && [ $stop_stage -ge 3 ]; then
    echo "Stage 3: Convert .wrd to characters"
    for split in ${splits}; do
        python ${working_dir}/utils/convert_chr.py \
            --in-path ${manifest_dir}/${split}.wrd \
            --out-path ${manifest_dir}/${split}.chr \
            --language ${lang} \
            --remove-punctuation
    done
    
    python ${working_dir}/utils/create_dict.py \
        --unit-paths ${manifest_dir}/train.chr ${manifest_dir}/dev.chr ${manifest_dir}/test.chr \
        --out-path ${manifest_dir}/dict.chr.txt
fi