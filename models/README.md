# Model files (not stored in Git)

The trained weights (`.pkl`) are **ignored by Git** on purpose:

- They are large (often hundreds of MB). GitHub **rejects files over 100 MB** in normal commits.
- Keeping them local avoids bloating every clone.

**For your machine:** keep `rf_model_v2.pkl` and `label_encoder.pkl` in this folder (same names as in `config.py`).

**For Render / sharing:** upload both files to a **[GitHub Release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)** as release assets, then set `MODEL_URL` and `ENCODER_URL` to the direct download links in your host’s environment variables (see `DEPLOYMENT.md`).
