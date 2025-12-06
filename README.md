# FalloutForXenia

Fallout 3 and New Vegas both have issues with rendering when emulated through Xenia. Usually this wouldn't really matter, as the PC builds are superior, but both of these games have builds which have been recovered from dev kits, which have minor or major features not present in the PC build.

Included are patched versions of Fallout_Release_Beta.xex from each of these builds.

There are some minor visual issues, the most noticable one being the use of dithered transparency. Water also appears as opaque, and doesn't have surface detail, but is preferable to rendering through everything. I found an alternate method to use "true" transparency, but it brought back a number of the other issues that were issues previously.

---

If for whatever reason you wish to patch your own files, first decrypt and decompress your xex with xextool, search for the bytes
```
89 7F 00 06 39 6B FF FF 2B 0B 00 0D 41 99 02 80 3D 80 82 28
```
then 4 bytes before that match (there should be only one, this pattern exists in every one I've checked) paste in the following bytes:
```
60 00 00 00 89 7F 00 06 39 6B FF FF 2B 0B 00 0D 41 99 02 80 48 00 02 34
```

for extended patch there are 2 more values to replace.

scan for
```
2B 0B 00 00 40 9A 04 D4 89 7F 00 86 2B 0B 00 00
```
replace with
```
2B 0B 00 00 40 9A 04 D4 48 00 02 CC 2B 0B 00 00
```
then scan for
```
89 7F 00 69 2B 0B 00 00 40 9A 00 3C 7F A4 EB 78
```
and replace with
```
89 7F 00 69 2B 0B 00 00 48 00 00 3C 7F A4 EB 78
```
