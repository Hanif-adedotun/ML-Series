#### FinBERT-LSTM: Deep Learning based stock price prediction using News Sentiment Analysis

This project is an implementation based on this [paper](https://arxiv.org/pdf/2211.07392)

---
#### Methodology
A Full explanation can be found in this [Medium article](https://medium.com/@devhanif/)


---
### To run the Flask App

- If you have a computer with a GPU, you can run the requirements file 
```pip install -r requirements``` 
and then run the main file 
```Flask/main.py``` 
to start the Flask server.

- The conternarized version of the Fask application is deployed on docker hub, and you can spin up the image [locally:](https://hub.docker.com/r/devhanif/btc-prediction).


---
### To Run each script to build your own model

Follow these steps to set up the project:

#### Step 1: Create a Virtual Environment

Open your terminal and navigate to the project directory. Then, run the following command to create a virtual environment:

 ```
python -m venv .venv
 ```

#### Step 2: Activate the Virtual Environment

Activate the virtual environment by running the following command:

- On Windows:
  ```
  .\.venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source .venv/bin/activate
  ```

#### Step 3: Install the Required Dependencies

Once the virtual environment is activated, install the required dependencies by running:
```
pip install -r requirements.txt
```

#### Step 4: Run the 1-get-btc-price.ipynb file

To get the Bitcoin price data, run the Jupyter notebook file `1-get-btc-price.ipynb`. This will fetch and save the Bitcoin price data to a CSV file.

#### Step 5: Run the 2-scrape-coindesk.py

Run the `2-scrape-coindesk.py` script to scrape news headlines from Coindesk. Set the date range to get the news headlines for the desired period. You can adjust the `start_date` and `end_date` variables in the script to specify the date range.

#### Step 6: Run the 3-sentiment-analysis.ipynb file

Run the Jupyter notebook file `3-sentiment-analysis.ipynb` to perform sentiment analysis on the scraped news headlines. This will combine the sentiment scores with the closing price data for Bitcoin.

#### Step 7: Run the 4-train-lstm-model.ipynb file

Run the Jupyter notebook file `4-train-lstm-model.ipynb` to train the LSTM model based on the data obtained from the previous steps. This will use the combined sentiment scores and Bitcoin price data to train a predictive model for Bitcoin prices.

#### Bonus Step: Analyze the Results

After completing the previous steps, you can use the `5-analysis.ipynb` file to perform a basic analysis of your data, model, and script outputs. This will help you visualize and understand the performance of your predictive model and the impact of sentiment analysis on Bitcoin price predictions.

To run the analysis, execute the Jupyter notebook file `5-analysis.ipynb`:



---
#### Test data vs predicted sample from trained model
![image](https://github.com/user-attachments/assets/09838fe2-0e41-44a7-9e8e-d0e435d4f785)
