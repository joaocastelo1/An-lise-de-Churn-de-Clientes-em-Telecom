export const metadata = {
  title: 'Telecom Churn Dashboard',
  description: 'Customer Churn Analysis Dashboard',
}

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR">
      <body style={{ margin: 0 }}>{children}</body>
    </html>
  )
}