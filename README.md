# Autotrader used car values
Web scraping and analysis of autotrader adverts, to build a used car pricing model

## Summary
- Wrote a web scraper to extract used car advert details from online marketplace for Audi A6's.
- Engineered features including age, mileage, fsh, quattro, engine size etc.
- With only 2 features (age and mileage) a tuned Support Vector Machine achieved R^2=0.911 and MAE=£1622.
- Best model overall model was again a tuned Support Vector Machine, with R^2=0.965 and MAE=£961.

[[Link to notebook](https://nbviewer.jupyter.org/github/adin786/autotrader-analysis/blob/main/autotrader_analysis.ipynb)]  [[Link to webscraper code](https://github.com/adin786/autotrader-analysis/blob/main/webscrape_at.py)]

### Table of Contents
1. [Data exploration results](#data-exploration-results)
2. [Modelling results](#modelling-results)
3. [Model comparison table (simple)](#model-comparison-table-simple-model)
4. [Model comparison table (complex)](#model-comparison-table-complex-model) 

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

## Model comparison table (simple model)
|    | name                      |    cv_mean |     cv_std |   mae_test |    mse_test |    r2_test |
|---:|:--------------------------|-----------:|-----------:|-----------:|------------:|-----------:|
|  0 | Linreg basic              | 0.802644   | 0.0124396  |    2245.16 | 9.48089e+06 | 0.812901   |
|  1 | Linreg with poly features | 0.878056   | 0.00745929 |    1736.65 | 5.41615e+06 | 0.893116   |
|  2 | Elastic-net               | 0.808763   | 0.0294758  |    2426.46 | 8.93401e+06 | 0.823693   |
|  3 | KNN basic                 | 0.888031   | 0.0146579  |    1745.24 | 4.919e+06   | 0.902927   |
|  4 | KNN with poly features    | 0.890029   | 0.0154029  |    1729.91 | 4.78117e+06 | 0.905647   |
|  5 | SVR alternative           | 0.00689301 | 0.0048019  |    5346.68 | 5.05368e+07 | 0.00268901 |
|  6 | SVR tuned                 | 0.896578   | 0.00670467 |    1622.79 | 4.52914e+06 | 0.91062    |
|  7 | Tree                      | 0.863705   | 0.0176042  |    1863.78 | 5.67888e+06 | 0.887931   |
|  8 | Forest                    | 0.865559   | 0.0174099  |    1866.68 | 5.68772e+06 | 0.887756   |

## Model comparison table (complex model)
|    | name                           |   cv_mean |     cv_std |   mae_test |    mse_test |   r2_test |
|---:|:-------------------------------|----------:|-----------:|-----------:|------------:|----------:|
|  0 | Linreg complex                 |  0.923708 | 0.0113085  |   1280.97  | 2.83365e+06 |  0.94408  |
|  1 | Linreg complex + poly features |  0.94751  | 0.00473454 |   1159.01  | 2.20182e+06 |  0.956548 |
|  2 | KNN complex                    |  0.943013 | 0.0100798  |   1184.57  | 3.06284e+06 |  0.939557 |
|  3 | KNN complex + poly             |  0.951666 | 0.00797216 |   1076.34  | 2.25113e+06 |  0.955575 |
|  4 | SVR complex                    |  0.960544 | 0.00256924 |    961.387 | 1.75286e+06 |  0.965408 |
|  5 | Tree complex                   |  0.916312 | 0.0210107  |   1427.26  | 3.79339e+06 |  0.92514  |
|  6 | Forest complex                 |  0.954217 | 0.00429592 |   1048.9   | 1.87811e+06 |  0.962937 |
