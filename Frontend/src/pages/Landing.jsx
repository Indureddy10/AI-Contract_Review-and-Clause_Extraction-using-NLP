import { useNavigate } from 'react-router-dom'
import Layout from '../components/Layout'

function Landing() {
  const navigate = useNavigate()

  return (
    <Layout>
      <div className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-8">
          Welcome to AI Product
        </h1>
        <button
          onClick={() => navigate('/register')}
          className="bg-black text-white px-8 py-3 rounded-lg hover:bg-gray-800 transition-colors font-medium text-lg"
        >
          Get Started
        </button>
      </div>
    </Layout>
  )
}

export default Landing
