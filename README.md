# nicogest

nicogest makes a digest of a video on Niconico douga based on its comments.

## Install

```
git clone https://github.com/lon9/nicogest.git
pip install -r requirements.txt
```

## Usage

### CLI

```
python nicogest.py [video_id]
```


### Embedding

```
from nicogest import Nicogest

nicogest = Nicogest()
nicogest.do(video_id)
```
