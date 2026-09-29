# Dataset setup

Obtain CSE-CIC-IDS2018 via the [Canadian Institute for Cybersecurity dataset page](https://www.unb.ca/cic/datasets/ids-2018.html). The page provides AWS-hosted files and currently documents AWS CLI access. Install AWS CLI, then from PowerShell download the archive tree to a temporary folder (replace `<your-region>` with an AWS region):

```powershell
aws s3 sync --no-sign-request --region <your-region> "s3://cse-cic-ids2018/" .\cse-cic-ids2018-download
```

Copy the generated flow CSV files into this project's `data/raw/` directory. Keep supplied CSV headers, including `Label`. The application reads all `*.csv` files there. The dataset is large; configure `training.max_samples` to a representative cap for a local demonstration. The cap is applied before the train/test split; preprocessing objects are fitted on training rows only. Follow the dataset page's citation requirements in reports and publications.

This dataset is network-flow data and is not captured from an operational 6G deployment.
