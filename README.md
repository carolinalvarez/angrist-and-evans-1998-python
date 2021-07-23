# OSE data science final project | Carolina Alvarez G. | Summersemester 2021

**Angrist, J.D., & Evans, W.N. (1998).** [Children and Their Parents' Labor Supply: Evidence from Exogenous Variation in Family Size](https://www.jstor.org/stable/116844?seq=1). *The American Economic Review*, 88(3). 450-477. 

Angrist and Evans (1998) focuse on the endogeneity problem arising when trying to estimate the labor-supply consequence of childbearing for women. The authors use an instrumental variable approach by exploiting the parental preferences for a mixed sibling-sex composition (i.e., children of different gender) to construct instrumental variables using same sex and twin variables. The findings of the paper is that IV estimates statistically significant and smaller than OLS, suggesting that OLS might exaggerate the effect of childbearing on labor-supply outcomes. For samples of all women and married women, the estimated coefficients of having a third child are negative, which suggest that childbearing has a negative effect on labor-supply.

The replication is carried on the main notebook from this repository. The auxiliary folder contains different functions made for the cleaning of 1980 and 1990 Census Extracts, data preparation, summary statistics, regressions and tables, and plots. It also contains pickled files for the results of simulations using causal forests as part as the proposed research extensions for estimating heterogenous treatment effects across different subgroups of schooling levels for women. To ensure the reproducibility of the proyect, the code for creating the pickled files can be found on the notebook as a code block.

My proposed extensions on Angrist and Evans (1998) are:

* Estimation of the probability of additional childbearing conditional to women's education
* A Causal Forest application for an alternative estimation of heterogeneity effects
* A test for selection on unobservables or "violation of exclusion restriction"

------------------------------------------------------------------------------------------------------------------------------------------------------------------

The notebook that contains my replication of the results of Angrist and Evans (1998) can also be visualized using nbviewer and mybinder under the following badges:

<a href="https://nbviewer.jupyter.org/github/OpenSourceEconomics/ose-data-science-course-project-carolinalvarez/blob/master/Angrist_and_Evans_1998.ipynb"
   target="_parent">
   <img align="center"
  src="https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.png"
      width="109" height="20">
</a>
<a href="https://mybinder.org/v2/gh/OpenSourceEconomics/ose-data-science-course-project-carolinalvarez/master?filepath=Angrist_and_Evans_1998.ipynb"
    target="_parent">
    <img align="center"
       src="https://mybinder.org/badge_logo.svg"
       width="109" height="20">
</a>

Also, my repository is supported by GitHub Actions Continuos Integration (CI). The state of my workflow can be found here:

</a>
<a href="https://github.com/OpenSourceEconomics/ose-data-science-course-project-carolinalvarez/actions/workflows/ci.yml"
    target="_parent">
    <img align="center"
       src="https://github.com/OpenSourceEconomics/ose-data-science-course-project-carolinalvarez/actions/workflows/ci.yml/badge.svg"
       width="200" height="20">
</a>
