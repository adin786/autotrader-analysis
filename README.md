# Autotrader used car values
Web scraping and analysis of autotrader adverts, to build a used car pricing model

## Summary
- Wrote a web scraper to extract used car advert details from online marketplace for Audi A6's.
- Engineered features including age, mileage, fsh, quattro, engine size etc.
- Trained a *simple* regression model based on only 'age' and 'mileage' features:
  - Best model was a tuned Support Vector Machine with an R^2 score of 0.911 on the testing set and mean absolute error of £1622.
- Trained a *complex* regression model based on all engineered features:
  - (in progress)

[[Link to notebook](https://nbviewer.jupyter.org/github/adin786/autotrader-analysis/blob/main/autotrader_analysis.ipynb)]  [[Link to webscraper code](https://github.com/adin786/autotrader-analysis/blob/main/webscrape_at.py)]

### Table of Contents
1. [Data exploration results](#data-exploration-results)
2. [Modelling results](#modelling-results)
3. [Model comparison table](#model-comparison-table) 

## Prerequisites
**Libraries used:** Pandas, Numpy, Requests, BeautifulSoup4, Matplotlib, Seaborn, Scikit-learn, 


 ## Data exploration results
![corrmat.png](/images/corrmat.png)

Some sellers choose to highlight when a car has full service history (or FSH).  *Note:* I did not search text within each advert's detail page, only the search page summary, so this feature was only true when the seller chose to highlight the service history in the `attention grabber` text.

Generally we'd expect this be appealing to buyers and increase the value... however **adverts with FSH mentioned turned out to be typically lower value than the ones which didn't mention it which was surprising...**

![](/images/fsh.png)

...On closer inspection **fsh only tended to be mentioned on older cars**.  So filtering the data down to those over 10 years old showed that the presence of "fsh" in the advert did **tend to correlate with higher prices, but only on older cars**.

![](/images/fsh10yr.png)

Model revision was calculated by binning the registration dates according to some dates from Wikipedia. This is therefore just a low fidelity abstraction of the `age` feature, but I thought it was valuable to include so the model could **pick up any "step" in pricing between consecutive model revisions**.  There wasn't much overlap in pricing between these categories (except in the much older model revisions) which made sense.

![](/images/modelrev.png)
...should insert scatter plot coloured according to model_rev classes

**Privately sold cars were generally lower value** than from trade sellers... **however privately sold cars were also typically older and higher mileage** than from trade sellers.  So there's some feature interactions behind this which aren't apparent from just looking at this one feature.  2nd row of plots provided below to show the distribution of age/mileage whether "private" or "trade" seller.

![](/images/privatevstrade.png)
![](/images/privatevstrade_agemileage.png)

**Adverts which mentioned "quattro" were slightly higher value**. Quattro is a feature that has been available on most modelyears of Audi A6, so this should apply across all ages of car.

![](/images/quattro.png)

## Modelling results
Trained 
- Simple model achieved 

## Model comparison table
|    | name                      |    cv_mean |     cv_std |   mae_test |    mse_test |    r2_test |
|---:|:--------------------------|-----------:|-----------:|-----------:|------------:|-----------:|
|  0 | Linreg basic              | 0.803      | 0.0124     |    2245    | 9.5e+06     | 0.813      |
|  1 | Linreg with poly features | 0.878      | 0.0075     |    1737    | 5.4e+06     | 0.893      |
|  2 | Elastic-net               | 0.809      | 0.0295     |    2426    | 8.9e+06     | 0.824      |
|  3 | KNN basic                 | 0.888      | 0.0147     |    1745    | 4.9e+06     | 0.903      |
|  4 | KNN complex               | 0.890      | 0.0154     |    1730    | 4.9e+06     | 0.906      |
|  5 | SVR (bad fit)             | 0.007      | 0.0048     |    5347    | 5.1e+07     | 0.003      |
|  6 | SVR tuned                 | 0.897      | 0.0067     |    1623    | 4.5e+06     | 0.911      |
|  7 | Tree                      | 0.864      | 0.0168     |    1890    | 5.8e+06     | 0.886      |
|  8 | Forest                    | 0.864      | 0.0176     |    1869    | 5.7e+06     | 0.888      |
