import styles from "@/styles/Footer.module.css";

export default function Footer() {
  return (
    <footer className={styles.footerPart}>
          <p>&copy; {new Date().getFullYear()} Мой сайт. Все права защищены.</p>
    </footer>
  );
}
