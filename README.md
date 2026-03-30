# cbs-youth-smoking-trends
Analysis and visualization of cigarette and e-cigarette trends among Dutch youth (age 16–19) using CBS public data

## Summary
This project analyzes how smoking and e-cigarette use among Dutch youth aged 16–19 changed from 2014–2025 using CBS Open Data (dataset 85457ENG: "Life style; personal characteristics"). 

Cigarette smoking among Dutch youth (16–19) fell from 23% in 2014 to 15.5% in 2018, then hovered around 15–20% through 2025. E-cigarette use wasfirst measured in 2019, and rose to 13% by 2025. Combined exposure to cigarettes and e-cigarettes increased from 2021, suggesting e-cigarettes offset cigarette reductions. E-cigarette exposure growth plateaued in 2024, likely due to the Dutch ban on sweet-flavored vapes. Monitoring all smoking products is key to understanding youth exposure trends to unhealthy habits.

## How to run the code
1. Clone the repository
<pre></>git clone https://github.com/MaartenKlavedijk/cbs-youth-smoking-trends.git
cd cbs-youth-smoking-trends</pre>
2. Install Python 3.9+ and dependencies:
<pre>pip install pandas matplotlib requests</pre>
3. Run the analysis script:
<pre>python main.py</pre>
4. Output:
<pre>youth_smoking_trends.png</pre>

## Data Source
CBS Dataset: 85457ENG: "Life style; personal characteristics". Accessed automatically in the code via the CBS API using requests in Python.
