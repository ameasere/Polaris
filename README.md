
<h1 align="center">
  <br>
  <a href="https://ameasere.com/polaris-fd5354/"><img src="https://i.imgur.com/XyFzezD.png" alt="polaris" width="200"></a>
  <br>
  <br>
</h1>

<h4 align="center">Open Source HSM configuration and management engine.</h4>

<p align="center">
  <a href="https://github.com/ameasere/polaris/releases">
    <img src="https://img.shields.io/github/v/release/ameasere/polaris?label=Release&logo=GitHub&sort=semver&style=for-the-badge">
  </a>
  <a href="https://github.com/ameasere/polaris/branches"><img src="https://img.shields.io/github/last-commit/ameasere/polaris?logo=GitHub&style=for-the-badge"></a>
  <a href="https://github.com/ameasere/polaris/releases/">
      <img src="https://img.shields.io/github/repo-size/ameasere/polaris?logo=GitHub&style=for-the-badge">
  </a>
  <a href="https://github.com/ameasere/polaris/blob/main/polaris.py">
    <img src="https://img.shields.io/github/license/ameasere/polaris?style=for-the-badge">
  </a>
</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#credits">Credits</a> •
  <a href="#related">Related</a> •
  <a href="#license">License</a>
</p>

<p align="center">
<img src="https://github.com/ameasere/Polaris/assets/55900441/610746f7-a4a7-41fe-b8ad-f270ef9c0a6b"

</p>

## Key Features

* Configuration, deployment and management of HSMs.
* Multiple HSMs can be managed at once. (Prospective)
* Accounts managed by Polaris can be used to log into the HSMs.
* NFC support for logging into HSMs in administrator mode. (Prospective)
* Secrets generation, storage and remote management without the worry of a man in the middle.

With advanced cryptography at its heart, Polaris maximizes the potential of data security even on the cheapest hardware; you can even deploy it on a VM, we wouldn't recommend it though.
Polaris keeps your data in the spotlight while ensuring only you and the HSM can communicate privately. Learn more about this from Cloudflare <a href="https://blog.cloudflare.com/a-relatively-easy-to-understand-primer-on-elliptic-curve-cryptography">here.</a>

## How To Use

To use Polaris:

* Download the latest release from [here](https://github.com/ameasere/polaris/releases) for your OS/Architecture.

* Source Code
  - Clone this repository via the Command Line with `git clone https://github.com/ameasere/polaris`.
  - Install [Python 3.8+](https://python.org) for your OS/Architecture, and add to your PATH.
  - Install the requirements via the `requirements.txt` file.
  - Modify the source code to fit your account management requirements (by default, Polaris uses the global
    server at `ameasere.com`).
  - Execute the `polaris.py` file via the Command Line, or using an IDE.
    - We highly recommend [PyCharm](https://www.jetbrains.com/pycharm/), that is how we developed Polaris!

## Open-Source

Please remember that this software is entirely **open-source**, meaning everything you see was developed for free with no financial incentive, investment or gain and was entirely done during personal time.

## Credits

This software uses the following:

- [Python](https://python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Qt](https://qt.io)
- [Mailgun](https://mailgun.com)
- [Doppler](https://doppler.com)
- [Mintlify](https://mintlify.com)
- [DRand](https://drand.love/)
- [Sentry](https://sentry.io)
- [CircleCI](https://circleci.com)
- Emojis are taken from [here](https://github.com/arvida/emoji-cheat-sheet.com)

With a huge thanks to:

- [Wanderson Pimenta](https://github.com/Wanderson-Magalhaes)
- [Zeno Rocha](https://zenorocha.com/)
- Dr Ahmed Elmesiry, PhD @ LMU

## Support

<a href="paypal.me/leighdb" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

## License

GPL-3 

---

> Developer [@ameasere](https://github.com/ameasere)
