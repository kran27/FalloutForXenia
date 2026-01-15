# FalloutForXenia

Fallout 3 and New Vegas both have issues with rendering when emulated through Xenia. Usually this wouldn't really matter, as there is essentially no reason to play the console versions, but both of these games have builds which have been recovered from dev kits, which have minor or major features not present in the PC build.

The recent New Vegas .pdb release allowed me to take a closer look at the rendering code of the engine, so using that I have created patched versions of Fallout_Release_Beta.xex from each of these builds.

Note that while these patches are targeting usage in the xenia emulator, they are not relevant to development of xenia. I am merely sidestepping the underlying issue, a "real" fix in xenia is well above my pay grade, and certainly not a trivial thing.

The patch fixes rendering issues present in xenia by forcing everything to render as if it was LOD. This is not a perfect solution, the most noticable degradations are missing water surface detail and transparency, along with translucent materials using ATOC (alpha to coverage) instead of "true" transparency, leading to a dithered presentation.

---

If you wish to patch your own files instead of using the versions provided here, download `xextool.exe` and `patch.py` from this repo, and run `python patch.py <xex_file>`. This script will produce the same files as are included in this repo.

This has only been tested on `Fallout_Release_Beta.xex` files, other build configurations are not supported.

---

The license in this repo applies only to the present code. No ownership or authorship is claimed of the xextool.exe binary, or any binaries present in previous commits, or GitHub releases.
