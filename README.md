<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
<div align="center">
  
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Twitter][twitter-shield]][twitter-url] 

</div>

<h3 align="center">Multilingual Customer Service Ticket Classification</h3>

  <p align="center">
    Classifying customer support tickets based on sentiment and urgency to improve resource allocation. <br />
    Notebooks are available to review the project with the provided dataset or visit the Flask app (https://csTicketUrgency.pythonanywhere.com) to test it out!
    <br />
    <br />
    <a href="https://github.com/keatonrproud/cs_ticket_urgency/issues">Report Bug</a>
    ·
    <a href="https://github.com/keatonrproud/cs_ticket_urgency/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

As more people get online and join the virtual marketplace, there is a larger expectation to provide high-quality customer service. Small businesses often don't have the funding required for a large customer service team and must maximize their resources. On top of this, more globalization means more customer feedback is in non-native languages and dealing with multilingual data becomes increasingly important. 

<br />

The biggest question is how do you prioritize all the customer service (CS) requests? This project looks to provide a straightforward solution. <b>Through sentiment analysis and urgency classification of multilingual CS requests, tickets are classified so the most critical and time-sensitive issues can rise to the top, regardless of the language they're submitted in. </b>

<br />

The English-only sample was originally obtained via [Kaggle](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter). The script used to create a multilingual (and significantly smaller) dataset for testing is the [build_translated_data.ipynb](https://github.com/keatonrproud/cs_ticket_urgency/blob/main/build_translated_data.ipynb) notebook. The reduced English-only and multilingual datasets used for building this project are available in this repo as parquet files.

Here's an example of the output on the provided sample input data:

![Sample Data](/screenshot.PNG)

### Built With

[![Python][python-shield]][python-url]
[![Jupyter Notebook][jupyter-shield]][jupyter-url]
[![PyCharm][pycharm-shield]][pycharm-url]
[![Flask][flask-shield]][flask-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

If you want an overview of the main code, [eval_requests.ipynb](https://github.com/keatonrproud/cs_ticket_urgency/blob/main/eval_requests.ipynb) is your best bet. 
Alternatively, clone the repo and access the scripts locally.

If you want to play around with the model's classifications, you can visit the [web app](https://csticketurgency.pythonanywhere.com) and insert your own data to see how it works firsthand. You can download the sample data from the flask_upload directory.

### Prerequisites

You'll need several packages to run the scripts directly -- _[deep-translator](https://pypi.org/project/deep-translator/), [numpy](https://numpy.org/), [pandas](https://pandas.pydata.org/), [luga](https://github.com/Proteusiq/luga), and [vaderSentiment](https://github.com/cjhutto/vaderSentiment)_. Of course, you'll need _[Flask](https://flask.palletsprojects.com/en/)_ if you intend on running the web app on your own.

Ensure you have all packages installed. 

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/keatonrproud/cs_ticket_urgency.git
   ```
2. Install any missing packages
   ```sh
   pip install missing_package
   ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

If you have a suggestion, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". All feedback is appreciated!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Kaggle](tps://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter) for the dataset.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Keaton Proud - [Website](https://keatonrproud.github.io) - [LinkedIn](https://linkedin.com/in/keatonrproud) - [Twitter](https://twitter.com/keatonrproud) - keatonrproud@gmail.com

Project Link: [https://github.com/keatonrproud/cs_ticket_urgency](https://github.com/keatonrproud/cs_ticket_urgency)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/keatonrproud/cs_ticket_urgency.svg?style=for-the-badge
[contributors-url]: https://github.com/keatonrproud/cs_ticket_urgency/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/keatonrproud/cs_ticket_urgency.svg?style=for-the-badge
[forks-url]: https://github.com/keatonrproud/cs_ticket_urgency/network/members
[stars-shield]: https://img.shields.io/github/stars/keatonrproud/cs_ticket_urgency.svg?style=for-the-badge
[stars-url]: https://github.com/keatonrproud/cs_ticket_urgency/stargazers
[issues-shield]: https://img.shields.io/github/issues/keatonrproud/cs_ticket_urgency.svg?style=for-the-badge
[issues-url]: https://github.com/keatonrproud/cs_ticket_urgency/issues
[license-shield]: https://img.shields.io/github/license/keatonrproud/cs_ticket_urgency.svg?style=for-the-badge
[license-url]: https://github.com/keatonrproud/cs_ticket_urgency/blob/main/license
[linkedin-shield]: https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white
[linkedin-url]: https://linkedin.com/in/keatonrproud
[twitter-shield]: https://img.shields.io/badge/Twitter-%231DA1F2.svg?style=for-the-badge&logo=Twitter&logoColor=white
[twitter-url]: https://twitter.com/keatonrproud
[python-shield]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://python.org/
[jupyter-shield]: https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white
[jupyter-url]: https://jupyter.org/
[pycharm-shield]: https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green
[pycharm-url]: https://jupyter.org/](https://www.jetbrains.com/pycharm/
[flask-shield]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[flask-url]: https://flask.palletsprojects.com/en/
