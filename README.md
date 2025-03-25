# 🏷️ Simple Open Coding Tool

This is a simple web-based tool designed to streamline dataset labelling, such as open coding, particularly for datasets containing links. Instead of manually opening URLs and switching between windows, this tool embeds links directly in a web-app. It has been successfully used in multiple projects for labelling GitHub Pull Requests.

## 📦 Dependencies
Ensure you have the following installed:

```sh
pip install flask pandas
```

Additionally, to embed GitHub into an iFrame, you must install the following Chrome extension:
[🔗 Ignore X-Frame Headers](https://chrome.google.com/webstore/detail/ignore-x-frame-headers/gleekbfjekiniecknbkamfmkohkpodhe)

## 🚀 How to Run
1. Open `app.py` and update the dataset path if needed. You can modify the path in the `dataset_path` variable:
   ```python
   dataset_path = "samples/dataset.csv"
   ```
2. Navigate to the root folder of this tool and run:
   ```sh
   flask run
   ```
3. Open your browser and go to:
   ```
   http://localhost:5000
   ```
4. Start labelling your dataset! You will see new ```label``` and ```comments`` columns appear in the CSV as you do labelling.

## 🔄 Notes
- Restart the tool (`flask run`) whenever you change the dataset.
- Use Google Chrome for the best experience.

🎉 **Happy labelling!**