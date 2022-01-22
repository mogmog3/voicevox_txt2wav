import requests
import json
import argparse
import os

def create_audio(word,fname_voice,fname_query,speaker):
    url = "http://localhost:50021/audio_query"
    params = {  "speaker":speaker,
                "text":word}
    req = requests.post(url,params=params)
    query = json.loads(req.text)
    with open(fname_query,"w") as f:
        f.write(req.text)

    params = {"speaker":speaker}
    url = "http://localhost:50021/synthesis"
    headers = {"Content-Type":"application/json"}
    req = requests.post(url,headers=headers,params=params,json=query)
    with open(fname_voice,"wb") as f:
        f.write(req.content)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input",dest="INPUT",type=str,nargs="*",required=True)
    parser.add_argument("--speaker",dest="SPEAKER",type=int,required=False,default=8)
    args = parser.parse_args()
    ifname_list = args.INPUT
    speaker = args.SPEAKER
    for ifname in ifname_list:
        #check to exist file
        if not(os.path.exists(ifname)):
            print(f"{ifname} is not existed. Skip the file.")
            continue
        #create save folder
        root_dir = os.path.join(os.path.splitext(ifname)[0])
        if not(os.path.exists(root_dir)):
            os.mkdir(root_dir)
        print(f"ROOT:{root_dir}")
        with open(ifname) as f:
            lines = f.readlines()
            lines = [i for i in lines if not(i=='\n')]
            for (no,line) in enumerate(lines,start=1):
                ofname_query =os.path.join(root_dir,f"query_{no:03}.json")
                ofname_voice =os.path.join(root_dir,f"voice_{no:03}.wav")
                print(ofname_voice,line.replace("\n",""))
                create_audio(
                        speaker=speaker,
                        word=line,
                        fname_voice=ofname_voice,
                        fname_query=ofname_query
                        )
    return 0

if __name__ == "__main__":
    main()

