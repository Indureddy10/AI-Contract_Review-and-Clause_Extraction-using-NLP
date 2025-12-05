import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Layout from '../components/Layout'

function Dashboard() {
  const navigate = useNavigate()
  const [uploadedFile, setUploadedFile] = useState(null)
  const [showSummary, setShowSummary] = useState(false)

  const handleFileUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      setUploadedFile(file)
      setShowSummary(true)
    }
  }

  const handleLogoutAndDelete = () => {
    navigate('/')
  }

  return (
    <Layout>
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-8 text-center">
          Dashboard
        </h1>

        <div className="max-w-4xl mx-auto space-y-6">
          <div className="bg-white shadow-lg rounded-xl p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Upload Documents
            </h2>
            <input
              type="file"
              onChange={handleFileUpload}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg cursor-pointer file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-black file:text-white hover:file:bg-gray-800 file:cursor-pointer"
            />
          </div>

          {showSummary && (
            <>
              <div className="bg-white shadow-lg rounded-xl p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">
                  Document Summary
                </h2>
                <div className="bg-gray-50 p-6 rounded-lg">
                  <p className="text-gray-600">
                    Summary will appear here...
                  </p>
                </div>
              </div>

              <div className="bg-white shadow-lg rounded-xl p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">
                  Important Clauses
                </h2>
                <div className="space-y-4">
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h3 className="font-semibold text-gray-900 mb-2">
                      Important Dates
                    </h3>
                    <p className="text-gray-600">
                      Details will appear here...
                    </p>
                  </div>

                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h3 className="font-semibold text-gray-900 mb-2">
                      Termination
                    </h3>
                    <p className="text-gray-600">
                      Details will appear here...
                    </p>
                  </div>

                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h3 className="font-semibold text-gray-900 mb-2">
                      Parties
                    </h3>
                    <p className="text-gray-600">
                      Details will appear here...
                    </p>
                  </div>

                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h3 className="font-semibold text-gray-900 mb-2">
                      Conclusion
                    </h3>
                    <p className="text-gray-600">
                      Details will appear here...
                    </p>
                  </div>
                </div>
              </div>
            </>
          )}

          <div className="bg-white shadow-lg rounded-xl p-8">
            <button
              onClick={handleLogoutAndDelete}
              className="w-full bg-red-600 text-white py-3 rounded-lg hover:bg-red-700 transition-colors font-medium"
            >
              Logout & Delete Account
            </button>
          </div>
        </div>
      </div>
    </Layout>
  )
}

export default Dashboard
