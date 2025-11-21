import { Link } from 'react-router-dom'

function Layout({ children }) {
  return (
    <div className="min-h-screen flex flex-col bg-white">
      <header className="bg-black text-white">
        <nav className="container mx-auto px-4 py-4">
          <ul className="flex space-x-6 items-center">
            <li>
              <Link to="/" className="hover:text-gray-300 transition-colors">
                Home
              </Link>
            </li>
            <li>
              <Link to="/register" className="hover:text-gray-300 transition-colors">
                Register
              </Link>
            </li>
            <li>
              <Link to="/login" className="hover:text-gray-300 transition-colors">
                Login
              </Link>
            </li>
          </ul>
        </nav>
      </header>

      <main className="flex-grow">
        {children}
      </main>

      <footer className="bg-black text-white py-6">
        <div className="container mx-auto px-4 text-center">
          <p>&copy; 2025 AI Product. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}

export default Layout
