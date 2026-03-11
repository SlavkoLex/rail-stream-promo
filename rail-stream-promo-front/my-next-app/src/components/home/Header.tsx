import styles from "@/styles/Header.module.css";
import headerBackgroundImage from '@/assets/pages/home/images/header/Image.png'
import logo from '@/assets/pages/home/images/header/logo.png'
import bar from '@/assets/pages/home/images/header/bar.png'

import Image from 'next/image';

export default function Header() {
  return (
    <header className={styles.headerPart}>

        <Image 
        src={headerBackgroundImage}
        alt="Description"
        fill
        style={{
          objectFit: 'cover',
          zIndex: 0,
        }}
        priority/>

        <div className={styles.imageOverlay}>

          {/* =============== Navigation ============== */}
          <nav className={styles.navContainer}>

            <div className={styles.navContactBlock}>
              <a href="" className={styles.styleNavTitle}>
                Контактная информация
              </a>
            </div>

            <div className={styles.navProductBlock}>

              <a href="" className={styles.styleNavTitle}>
                О продуктах
              </a>
            </div>

            <div className={styles.logoBlock}>
                <Image 
                src={logo}
                alt="Description"
                fill
                style={{
                  objectFit: 'cover',
                }}/>
            </div>

          </nav>

          {/* ================== Text ===================*/}

          <div className={styles.textContainer}>

            <div className={styles.sloganBlock}>
                <p className={styles.sloganPromoTextStyle}>
                  цифровизация и автоматизация путей <br></br> железнодорожного сообщения
                </p>
                <p className={styles.sloganMainTextStyle}>
                  Железные дороги <br></br> Умные решения
                </p>
            </div>

            <div className={styles.barBlock}>
              <Image 
                src={bar}
                alt="Description"
                fill
                style={{
                  objectFit: 'cover',
                }}/>
            </div>

            <div className={styles.companyNameBlock}>
                <p className={styles.companyNamePromoTextStyle}>
                  научно-внедренческий центр
                </p>
                <p className={styles.companyNameMainTextStyle}>
                  БЕЗОПАСТНОСТЬ ТРАНСПОРТА
                </p>
            </div>

          </div>

        </div>


    </header>
  );
}
