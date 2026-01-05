#!/usr/bin/env bash

rg --pcre2 --encoding shift_jis "^(ProjectName|VoiceDir|OutFile|CacheDir|Tool1|Tool2|Label)=(?!wavtool\.exe|resampler\.exe|新規プロジェクト|New Project|newfile\.wav|\s+$)" *.ust *.ustx