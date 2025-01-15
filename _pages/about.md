---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% if site.google_scholar_stats_use_cdn %}
{% assign gsDataBaseUrl = "https://cdn.jsdelivr.net/gh/" | append: site.repository | append: "@" %}
{% else %}
{% assign gsDataBaseUrl = "https://raw.githubusercontent.com/" | append: site.repository | append: "/" %}
{% endif %}
{% assign url = gsDataBaseUrl | append: "google-scholar-stats/gs_data_shieldsio.json" %}

<span class='anchor' id='about-me'></span>

My research field is Process System Engineering(PSE). 

I have published 2 paper with total <a href='https://scholar.google.com/citations?user=2Ruek5kAAAAJ'><img src="https://img.shields.io/endpoint?url={{ url | url_encode }}&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>.



<span class='anchor' id='-edu'></span>

# 📖 Education
- *2023.08 - Now*, Ph.D. in Chemical Engineering, Tsinghua University, Beijing, China.
- *2019.09 - 2023.06*, Bachelor of Chemical Engineering, Tsinghua University, Beijing, China.


<span class='anchor' id='-pub'></span>

# 📝 Publications 

- [An Efficient Approach for Droplet Coalescence Videos Processing based on Instance Segmentation and Multi-Object Tracking Algorithms](https://www.sciencedirect.com/science/article/pii/B9780443288241505019)
  
  **Wenle Xu**, Shuyuan Zhang, Kai Wang, Tong Qiu
  <details>
    <summary>Abstract</summary>
    Controlled coalescence of droplets is a crucial method of performing reactions and synthesises within droplets. Among all methods employed for droplet characterization within microchannels, microscopic imaging stands out for its capacity to capture ample information. However, the processing of images and videos still predominantly relied on massive manual works, which falls short of meeting the demands for high-throughput analysis. To address this problem, this paper proposes an efficient approach based on instance segmentation and multi-object tracking algorithms to analyse the droplet coalescence videos in microchannels. This approach initially segments droplets in microscopic images and consequently associate the identical droplets and recognize the coalescence processes across consecutive frames. Finally, further analysis of these data can yield critical statistics of the droplet coalescence process, such as coalescence probability and coalescence time. This approach enables automated and efficient analysis of videos to decipher the droplet coalescence process, thereby accelerating the discovery and exploration of droplet coalescence patterns in microfluidics.
    
    <div style="text-align: center;">
      <img src="./images/coalescence.png" alt="coalescence" style="width: 80%;"/>
    </div>

  </details>

- [Integrated Hybrid Modelling and Surrogate Model-Based Operation Optimization of Fluid Catalytic Cracking Process](https://www.mdpi.com/2227-9717/12/11/2474)
  
  Haoran Li, Qiming Zhao, Ruqiang Wang, **Wenle Xu**, Tong Qiu
  <details>
    <summary>Abstract</summary>
    Fluid Catalytic Cracking (FCC) is one of the most important conversion processes in oil refineries, widely used to convert high-boiling, high-molecular-weight hydrocarbon components from crude oil into more valuable products like gasoline and diesel. Advanced simulation and optimization technologies are critical for improving the operational efficiency and economic performance of the FCC process. First-principles-based simulators rely on parameter estimation and are computationally intensive, making them unsuitable for online optimization. In recent years, with the development of deep learning, data-driven models have made significant progress in FCC modeling. However, due to their black-box nature and difficulty with extrapolation, they are rarely used for optimization. To bridge this gap, we propose an integrated framework that combines hybrid modeling and surrogate model-based optimization. This approach combines plant and simulation data to train a multi-task learning prediction model, which then serves as a surrogate for operational optimization. Validated on a large-scale FCC unit in southern China, the model predicts product yields with an error margin of under 4.84% for all products. Following optimization, yields of LNG, gasoline, and diesel rose by an average of 0.10 wt%, 1.58 wt%, and 1.05 wt%, respectively, resulting in a 3.67% increase in product revenues. This highlights the substantial potential of this framework for industrial applications.

    <div style="text-align: center;">
      <img src="./images/processes-12-02474-g001.png" alt="FCC" style="width: 80%;"/>
    </div>
  </details>

<span class='anchor' id='-award'></span>

# 🏅 Honors and Awards
- *TODO* 🤔


<span class='anchor' id='-intern'></span>

# 💻 Internships
- *None* 🤔