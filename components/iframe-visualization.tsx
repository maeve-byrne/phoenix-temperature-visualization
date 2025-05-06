"use client"

import { useState, useEffect } from "react"

export default function IframeVisualization() {
  const [isLoading, setIsLoading] = useState(true)
  const [hasError, setHasError] = useState(false)
  const [iframeHeight, setIframeHeight] = useState("600px")

  useEffect(() => {
    // Adjust iframe height based on window size for better responsiveness
    const updateHeight = () => {
      const height = window.innerWidth < 768 ? "400px" : "600px"
      setIframeHeight(height)
    }

    updateHeight()
    window.addEventListener("resize", updateHeight)

    return () => window.removeEventListener("resize", updateHeight)
  }, [])

  return (
    <div className="w-full border rounded-lg overflow-hidden bg-white relative">
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-white z-10">
          <div className="text-center p-4">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p>Loading visualization...</p>
          </div>
        </div>
      )}

      {hasError && (
        <div className="absolute inset-0 flex items-center justify-center bg-white z-10">
          <div className="text-center p-4 text-red-500">
            <p>Error loading visualization. Please try refreshing the page.</p>
            <button
              onClick={() => window.location.reload()}
              className="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Refresh
            </button>
          </div>
        </div>
      )}

      <iframe
        src="/visualization/index.html"
        className="w-full border-0"
        style={{ height: iframeHeight }}
        title="Phoenix Temperature Visualization"
        onLoad={() => {
          console.log("Visualization iframe loaded")
          setIsLoading(false)
        }}
        onError={() => {
          console.error("Error loading visualization iframe")
          setIsLoading(false)
          setHasError(true)
        }}
        allowFullScreen
      />
    </div>
  )
}
