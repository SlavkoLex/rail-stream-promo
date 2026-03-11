import { Inter } from "next/font/google";

import Header from "@/components/home/Header";
import Footer from "@/components/home/Footer";
import EmergencePage from "@/components/effects/Emergence";

import "@/app/globals.css";

const inter = Inter({ subsets: ["latin", "cyrillic"] });

export default function HomeLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ru">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className={[inter.className, 'body'].join(' ')}>
        <EmergencePage>
          <div className="flex-main-container">

            <Header />

            <div className="home-page-content">
              <main>{children}</main>
            </div>

            <Footer />

          </div>
        </EmergencePage>
      </body>
    </html>
  );
}
