import './globals.css'

export const metadata = {
  title: 'Telecom Churn Dashboard',
  description: 'Customer Churn Analysis Dashboard',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}