# Algothon 2024 - Quantitative Portfolio Allocation Challenge

# A copy of our Algothon 2024 project with sensitive information removed 

## 🚀 Project Description
This project was developed for Algothon 2024, a leading quantitative hackathon hosted by the Algorithmic Trading Society at Imperial College London. Our challenge was to solve a portfolio allocation problem, where the goal was to maximize the performance of a portfolio by dynamically allocating weights to a set of trading strategies based on their log returns over time.

## What our application does
Our solution focused on implementing a dynamic portfolio allocation model using advanced quantitative techniques to optimize returns in real-time. We were provided with data in the form of dataframes, each representing the log returns (pnl) of various trading strategies over time. The twist was that data was released at regular intervals (approximately every 19 minutes), requiring us to continuously update our model's predictions to adapt to new data.

## Why we used the technologies we used
- Black-Litterman Model: We leveraged the Black-Litterman model to enhance our portfolio allocation strategy. Traditional Modern Portfolio Theory (MPT) relies heavily on historical mean and variance, which can be unreliable in the presence of noisy data. By incorporating market views and using the Black-Litterman approach, we were able to refine our predictions and optimize the allocation of weights across strategies.
Automated Trading & Submission Pipeline:

- To streamline our trading process, we built an automated system using APIs (Slack API, Google API Client) and Selenium for browser automation. This allowed us to submit our trade decisions seamlessly via a Google Form, minimizing delays and improving our overall efficiency.

## 🛠️ Technologies Used
- Python: Core language for data analysis, modeling, and automation.
- Pandas & NumPy: For efficient data manipulation and numerical calculations.
- APIs (Slack, Google API Client): For automated communication and trade submission.
- Selenium: For browser automation to handle Google Form submissions.

## 🤝 Credits
### Ishaan
Github: https://github.com/IshaanVyasIMP
Linkedin: https://linkedin.com/in/ishaan-vyas-iv2004

### Soong
Github: https://github.com/soongenwong
Linkedin: https://linkedin.com/in/soongenwong

### Alex
Github: https://github.com/moosemorse
Linkedin: https://linkedin.com/in/alexander-ivanov24
