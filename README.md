# time-taken-experiment

This repository contains some experiments that track how long training might take
in Rasa NLU. To get started with this you will need to install some dependencies.

```
make install
```

Once that is done, you'll want to generate the datafiles.

```
make data
```

This will generate a file structure like; 

```
📂 /home/vincent/Development/time-taken-experiment/data
┣━━ 📂 clean-100 
┃   ┗━━ 📄 clean.yml (693.8 kB)
┣━━ 📂 clean-150 
┃   ┗━━ 📄 clean.yml (1.0 MB)  
┣━━ 📂 clean-50  
┃   ┗━━ 📄 clean.yml (346.6 kB)
┣━━ 📂 typod-100 
┃   ┣━━ 📄 clean.yml (693.8 kB)
┃   ┗━━ 📄 typod.yml (698.8 kB)
┣━━ 📂 typod-150 
┃   ┣━━ 📄 clean.yml (1.0 MB)  
┃   ┗━━ 📄 typod.yml (1.0 MB)  
┗━━ 📂 typod-50  
    ┣━━ 📄 clean.yml (346.6 kB)
    ┗━━ 📄 typod.yml (349.1 kB)
```

Given these files you can now start training.

```
make train
```

And generate some summary statistics.

```
make stats
```

You can also just run everything in one go. 


```
make all
```
