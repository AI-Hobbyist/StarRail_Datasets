import click, shutil, os, librosa, re
from pathlib import Path
from glob import glob
from tqdm import tqdm
from pypinyin import lazy_pinyin, load_phrases_dict

personalized_dict = {
    '嗯': [['en']],
    '八重': [['ba'], ['chong']],
    '重云': [['chong'], ['yun']],
    '平藏': [['ping'], ['zang']]
}
load_phrases_dict(personalized_dict)

def get_length(src: str):
    wave_len = librosa.get_duration(path=src)
    return wave_len

def check(content):
    if re.search(r"[<>{}]", content):
        return True
    else:
        return False

@click.command(help='复制音频以及对应标注')
@click.option('--src', required=True, help='源目录')
@click.option('--min', default=2, help='最短音频（默认2秒）')
@click.option('--max', default=20, help='最长音频（默认20秒）')
@click.option('--dst', required=True, help='目标目录')
def copy_wav(src,min,max,dst):
    files = glob(f"{src}/*.wav")
    for file in tqdm(files):
        wav_len = get_length(file)
        if wav_len >= min and wav_len <= max:
            wav_file = os.path.basename(file)
            lab_file = wav_file.replace(".wav",".lab")
            spk_name = os.path.basename(os.path.dirname(file))
            text = Path(f"{src}/{lab_file}").read_text(encoding='utf-8')
            if check(text) == False:
                if os.path.exists(f"{dst}/{spk_name}") == False:
                    os.makedirs(f"{dst}/{spk_name}")
                pinyin = " ".join(lazy_pinyin(text, errors='ignore'))
                Path(f"{dst}/{spk_name}/{lab_file}").write_text(pinyin, encoding="utf-8")
                shutil.copy(f"{src}/{wav_file}",f"{dst}/{spk_name}/{wav_file}")
if __name__ == '__main__':
    copy_wav()