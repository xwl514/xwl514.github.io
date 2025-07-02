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

My research field is Process System Engineering(PSE) <a href='https://scholar.google.com/citations?user=2Ruek5kAAAAJ'><img src="https://img.shields.io/badge/2-9cf?label=%F0%9F%93%9Dpapers&labelColor=white"></a> 
<a href='https://scholar.google.com/citations?user=2Ruek5kAAAAJ'><img src="https://img.shields.io/endpoint?url={{ url | url_encode }}&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>.


<span class='anchor' id='-edu'></span>

# 📖 Education

 [![Tsinghua University][thu-logo]](https://www.tsinghua.edu.cn/) *2023.08 - Now*, Ph.D. in Chemical Engineering, Tsinghua University, Beijing, China.

 [![Tsinghua University][thu-logo]](https://www.tsinghua.edu.cn/) *2019.09 - 2023.06*, Bachelor of Chemical Engineering, Tsinghua University, Beijing, China.



<span class='anchor' id='-pub'></span>


# 📝 Publications 

 [An Efficient Approach for Droplet Coalescence Videos Processing based on Instance Segmentation and Multi-Object Tracking Algorithms](https://www.sciencedirect.com/science/article/pii/B9780443288241505019)
  
  **Wenle Xu**, Shuyuan Zhang, Kai Wang, Tong Qiu
  <details>
    <summary>Abstract</summary>
    Controlled coalescence of droplets is a crucial method of performing reactions and synthesises within droplets. Among all methods employed for droplet characterization within microchannels, microscopic imaging stands out for its capacity to capture ample information. However, the processing of images and videos still predominantly relied on massive manual works, which falls short of meeting the demands for high-throughput analysis. To address this problem, this paper proposes an efficient approach based on instance segmentation and multi-object tracking algorithms to analyse the droplet coalescence videos in microchannels. This approach initially segments droplets in microscopic images and consequently associate the identical droplets and recognize the coalescence processes across consecutive frames. Finally, further analysis of these data can yield critical statistics of the droplet coalescence process, such as coalescence probability and coalescence time. This approach enables automated and efficient analysis of videos to decipher the droplet coalescence process, thereby accelerating the discovery and exploration of droplet coalescence patterns in microfluidics.
    
    <div style="text-align: center;">
      <img src="./images/coalescence.png" alt="coalescence" style="width: 80%;"/>
    </div>
  </details>

<br>

 [Integrated Hybrid Modelling and Surrogate Model-Based Operation Optimization of Fluid Catalytic Cracking Process](https://www.mdpi.com/2227-9717/12/11/2474)
  
  Haoran Li, Qiming Zhao, Ruqiang Wang, **Wenle Xu**, Tong Qiu
  <details>
    <summary>Abstract</summary>
    Fluid Catalytic Cracking (FCC) is one of the most important conversion processes in oil refineries, widely used to convert high-boiling, high-molecular-weight hydrocarbon components from crude oil into more valuable products like gasoline and diesel. Advanced simulation and optimization technologies are critical for improving the operational efficiency and economic performance of the FCC process. First-principles-based simulators rely on parameter estimation and are computationally intensive, making them unsuitable for online optimization. In recent years, with the development of deep learning, data-driven models have made significant progress in FCC modeling. However, due to their black-box nature and difficulty with extrapolation, they are rarely used for optimization. To bridge this gap, we propose an integrated framework that combines hybrid modeling and surrogate model-based optimization. This approach combines plant and simulation data to train a multi-task learning prediction model, which then serves as a surrogate for operational optimization. Validated on a large-scale FCC unit in southern China, the model predicts product yields with an error margin of under 4.84% for all products. Following optimization, yields of LNG, gasoline, and diesel rose by an average of 0.10 wt%, 1.58 wt%, and 1.05 wt%, respectively, resulting in a 3.67% increase in product revenues. This highlights the substantial potential of this framework for industrial applications.

    <div style="text-align: center;">
      <img src="./images/processes-12-02474-g001.png" alt="FCC" style="width: 80%;"/>
    </div>
  </details>

<br>

 [MicroFlowSAM: A Motion-Prompted Instance Segmentation Approach in Microfluidics with Zero Annotation and Training](https://www.sciencedirect.com/science/article/pii/S1004954125002381)
  
**Wenle Xu**, Lin Sheng, Tong Qiu, Kai Wang, Guangsheng Luo
  <details>
    <summary>Abstract</summary>
    Microdispersion technology is crucial for a variety of applications in both the chemical and biomedical fields. The precise and rapid characterization of microdroplets and microbubbles is essential for research as well as for optimizing and controlling industrial processes. Traditional methods often rely on time-consuming manual analysis. Although some deep learning-based computer vision methods have been proposed for automated identification and characterization, these approaches often rely on supervised learning, which requires labeled data for model training. This dependency on labeled data can be time-consuming and expensive, especially when working with large and complex datasets. To address these challenges, we propose MicroFlowSAM, an innovative, motion-prompted, annotation-free, and training-free instance segmentation approach. By utilizing motion of microdroplets and microbubbles as prompts, our method directs large-scale vision models to perform accurate instance segmentation without the need for annotated data or model training. This approach eliminates the need for human intervention in data labeling and reduces computational costs, significantly streamlining the data analysis process. We demonstrate the effectiveness of MicroFlowSAM across 12 diverse datasets, achieving outstanding segmentation results that are competitive with traditional methods. This novel approach not only accelerates the analysis process but also establishes a foundation for efficient process control and optimization in microfluidic applications. MicroFlowSAM represents a breakthrough in reducing the complexities and resource demands of instance segmentation, enabling faster insights and advancements in the microdispersion field.

    <div style="text-align: center;">
      <img src="./images/cjche-0.jpg" alt="MicroFlowSAM" style="width: 80%;"/>
    </div>
  </details>
  
<span class='anchor' id='-award'></span>

# 🏅 Honors and Awards

- Second Prize for Excellent Paper (Chinese Annual Conference of Process System Engineering 2024, CPSE2024)
- Tsinghua University Outstanding Undergraduate Thesis (Top 5 out of all department graduates, 2023)
- Tsinghua University Academic Excellence Scholarship (2021-2022)
- Tsinghua University Academic Excellence Scholarship (2020-2021)




<span class='anchor' id='-intern'></span>

# 💻 Internships

 *None* 🤔

[thu-logo]: https://img.shields.io/badge/Tsinghua%20University-white?logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAFzUkdCAK7OHOkAAAAEZ0FNQQAAsY8L%2FGEFAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm%2B48GgAACuBJREFUWEeNV3lwVdUZ%2F845974tCwlhS0AwLAphBJsQIIAoavEPsVYpdtyqoySxVqw1iUO3oXScqRUS0LYsCTjSDVv%2BsK06VaogrSYIBNwAUcJqAkFDyPLy3n33nvP1dx6JU7DUfjNvuWf5zrf8vt93rqD%2FUx6gmiwZNqX4e4WS9DmznMhsMvDcKoXoNoLzyMguEtSSSJo9v6faeHrjV8hXGlAZ%2FcFIQ2qmMFQiJO3WhrsEiXnYaJioTRAzfkfZtTDkMLE8RYKHGOYcKfXf1idWtaYVXUIuaUAFLYtxtLdSsPiMWUSI2MWZnsAhXjJ4fxM9c65%2FKS2hJWEvEhtOrIuwLt%2BOsRAevsfDoE%2BFF3uhnpb3pRdfJLL%2F9wL5bnjpWIrEa8iI%2FYLpSmZ9%2Bpx3vJ6lsxU2j46EnYX9S9OSjIQXMgf%2Fwt%2Blvpt62fMyN2PfWRjfiaj1cKivfHG4qvD86gvlSwZUhB6fqGXwDUHmY4R3rIw4dRtSdS%2FnUlFYsPk5E%2F%2FEkOTy2GNpTytDNRME80NC0Md4bB%2FdO7hzEy1P1nsrXyXXbGZjhpM0Z3HQTQ%2BFaq60e%2F5TLjCgPFw9joS8gQ0l2IhezwteWNv1VKedsyF0OHgSmV%2BbTodWj9rxEalYiyF%2BDpHxWXCsLRq%2F1Y5b0HJK3FXgZa4Dfs4xyQBAnf9ApGqMnR%2BQLzBgc46wP4SBzwGiPmPEOfy%2FB1NnccCvNni1Rysj1d8RRryTSlFbKKbHG1aKyCcRCN%2B4fKahb%2FUpq2sRLVK54dFPAZ9vGyGHKsmd0NeNKA3D9KiMpH5mFa1K2LVfRIDDPXcJwSeM4RwywR4YcQcLKgDCL9Ok04YaKT5ECiaqMN%2BltZzOhksFO0WkRJEw7oPloaqby90nrtpCWzRcewlALMYBD%2BDwJU7E2W0QPpTM3t6QLE8fCoEHRIujT4xSJOZi0jGu%2F%2BeGxLOt05yyyWRoPwlRSE7wl%2Blq7jdR9%2FlGwhoWMc3iTaHkOSV12%2FpE3eslcuYZpC8LpXf5NGfOVb7j7XJMKMXCfA3W78uMmzcSgfpYOXSvUPRRaXhWxx6%2FKZ42YJoquw9FfMywaduYWP2eHVsQzG%2FsC3ueCru%2FRS4XYb4HadwuWVVA4URES5LQp0RAfnFodgWCWYZ4nvGd0HZp9ASpZVE04r%2BhfdlUn6rd3ERNqX3UmCpxZrlwIM9oyt6rmw7Lu2lJNsDTDSRHfa9jhz18cejxBctpuVnXV7dPJ%2Fw58AI1b7QRxmD6Taz%2FDGR0DcAV1Yg%2FSi4kBWXgeYpjEg4J0wvrIsmUO299qvYA9rBNj9Wd72VshZIoHJpWQRUxgfq8HmQRI6kHbUjW%2FcEuGpCKSHUZ9s5xkom1vhsuRIhH4%2FCAlGyXLC4XmlK2zo3RecBHSBK3gahGMOljMPAUG3kLK7mroW%2FF3n6VaamM1NwJfCVApR2qxJk9HxaHBalPi50yUapmX1ssZ4T2mp1nStyy6cBNh3bcpUJICcQchqe5AFOfZB6CJJyCQb6QIgeccZqEyhdCfQLm%2FDqTGMpCfgLumLg3aHrPgrM4XDZ7hjMzDkgHNpiI0gTQN2fja5TrxXfbUmMlWhkMYusVtTuGpYjAG0SNJ%2BD7FuQucIyM5Seztkgyn%2BLT1pk48Vdi1Ab6hDHB1Si%2FXgB6ihQ6D2Wba3WpkG4HqIc4Sf9MKhEcgoHXajQ1OCJ68SDW0Jp4ZaTqDiD9%2Fg3%2B0%2FtdpkKp%2BYhi7oSXryFyvmT5O4TfXeet3GExwkbdbrRcaMuu3luxTUo4Y2Qj6GUeyg%2F0AU4hblHEIzvimeAVLkqGQtf39xGDNE6C8wAE8TEMIC3oZFKC1exuKbAiin7QCtQfR44bAcZ85Le1IvzEdRWRqn%2BAE36Eev%2Bh%2FV8errkO0WwB2xXCiU3I1zbWThf0xaBj0BZaDsYSVn9%2FU%2BITIIUcRABkk%2B52GDKUJbSZmp63wmJQoCRyDt%2BN6dbMmQpU0eCt2A6SWWcB1%2F9ZY8d8H8WHKAAvSUNBIJTOtb0Annkw1uo7i0Mmp3ULQJjoqMWADc1IOwZwId2oeRsMdCMAqF0m5fuO1L2o87khR%2B4hbdJNSBhcQIiRe34ReLIUi%2ByYob6WH2BfppHOISPUERx8REnVaxVi%2FXiluCm9n%2BRlqJqUKI9WL4TnUxKeV5sRjVzPWo8RKfd5GfPHIjLjtEFbFXQ7tsRwWBc%2B2xHiFiLH3eCvfNfqWuxWTwXiPbDgVBi4n5R6BIe9hYpJAMgCbeigdsATTE8iik9ne%2FxWPKx%2BCis%2BVyVq1lyAZI%2Fjyjwwxz9RcjcbRTI%2FmdnYpfwyhKgNzDUPi1NkzDoovwxlh49MlsqyjFI1ZzCwMlxIcwXybokqCmN2Iwq4oCjbnKaMSGW82OX46ILipEPOPt%2BlK5E2Dzzgo7j5EOp5MDJUeNr%2BCBrElGp5Mx0mOo62PNQNOY9oaX4j0HTQTtqQjmNs9ClgY3yguAj1PEkynYaBfSjjkHacj5D7JhiWbYTYdoAOgP7pRpw1a4QXOQH8FEBPhyNEi5qq53SAYG5HjryxOrSnS%2BojSsgfDwkljolkb7NwQqVA63AoyAPRHEV53YlnGCpHw%2Fpj8KQTngyDsYOhuAMRa1dBMEk4chh4Y2gqmfFaRjRaDHduQF39LBXEvUCJ6ZbY4kmzAzW3okehRQIsQVuo96aNqacPQv8uw3KCGjQ4jNBuBUYKNJJZn1jRDLJ5FcaCnyjPkHAQKCs%2BIogQ8zy7BinKhUHoW%2FolJ7sb2BE3gjQ2JxPZHX1hd66lYVuC9uac7obF4endQGUBNk0r0XObM3Ww21fyHtacVZ%2Bse3uqW3YGpDEVnSyXlTkHLwEbxEDKVijTiv2DuC%2BOQc4OTnNnT4Z9HgryQy%2BZddqloBqGjUOKXvFjPb6rXfCFGEZK%2F2mvvxNNC2JvMtBXAAVbTUTfev62Il%2FG1Cg0pGXPJWuPC0%2F9EZWpwV9XIwFZANohw3oS8n6FIXc8aWpB38hHK%2B4OJ1KvS4e7wpH4t2BgANJfU5%2BqOxRNRRah8Z1AJbUP3J7SEbBSFJS97zriblh7pliVjURfeL00NDMONog068Z3m%2Bltr1k3HZ2ReW2L1oSeziHQk4cLCrCPUxzdqpLujvV65f5dtMsrdmYMQhkvQKTeafBqt%2BNCugCgdNE9C0SyZ1MzNfv2XMsOX4htGkDmbSCZHgDrdEOq9hUM2zVIMe4J7mOTN%2FirDzyY8eiwjfFn2zGMufMqvpe1dPCve35x9uFI1ai1ybqT6cF%2BwWV3Pn4KsdJRFPx9rbf6yPmZiwywYq%2FZuHignXIfrmkqCJsXN3avOmvnFkdqrkEW2kEt98O7naBDe19oAVF9BFWzUZaN8DA%2B0P%2Fvo%2B%2FnpN8hBC6txuQqFm%2Bs82s%2FtHMD8iUDrKQjYcRtrOgk%2BHmYJHnY93inrRg7XxmqKvJxkDJyqivNe0mMuYYy%2Bm8%2FtIyWObaicPA1eNwGup8Ogzc3eCvBoBfKfzXAyn20LBKK9H4b1TES7fiQ5X6UHTiLToKYdg%2FpCXfalty%2FXNyLFMRS%2FlXoMOMQhWxgpw91320JLispnqm9xMvqJQ0YkIdj1SO05ptxi%2BmR9oVFUg4QMQ5bXTSx46iICFIwEjQBPJrXWHIO2LNYSP4gxbTz%2BYvwcLF8pQEDYl9cZKSvBAQyDl5l4dAu%2B0puqRq80AtNn9jWC6MOkufuqadfdvVv%2FR9C9G9FCXTm9HyLtgAAAABJRU5ErkJggg%3D%3D
