"use client"

import Link from "next/link"
import { ExternalLink } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useState } from "react"
import IframeVisualization from "@/components/iframe-visualization"

export default function Home() {
  // State to track if YouTube iframe is loaded
  const [videoLoaded, setVideoLoaded] = useState(false)

  return (
    <div className="flex flex-col min-h-screen">
      <header className="bg-white border-b">
        <div className="container flex items-center justify-between h-16 px-4 md:px-6">
          <Link href="/" className="flex items-center gap-2 font-semibold">
            <span>Phoenix Climate Data</span>
          </Link>
          <nav className="hidden md:flex items-center gap-6 text-sm">
            <Link href="#visualization" className="font-medium">
              Visualization
            </Link>
            <Link href="#resources" className="text-muted-foreground hover:text-foreground transition-colors">
              Resources
            </Link>
          </nav>
        </div>
      </header>

      <main className="flex-1">
        {/* Header Image Section */}
        <section className="w-full">
          <div className="relative">
            <img
              src="/images/climate-phoenix-header.png"
              alt="Phoenix Climate and Sustainability"
              className="w-full h-[300px] object-cover"
            />
            <div className="absolute inset-0 bg-black/30 flex items-center">
              <div className="container px-4 md:px-6">
                <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-2">
                  Phoenix Climate Data <span className="block text-xl md:text-2xl mt-1">by Maeve Byrne</span>
                </h1>
                <p className="text-white/90 max-w-[700px] text-lg">
                  An analysis of the temperatures in the Phoenix metropolitan area in the years 1990 and 2024.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Visualization Section */}
        <section id="visualization" className="py-8 md:py-12">
          <div className="container px-4 md:px-6">
            <Card className="overflow-hidden">
              <CardHeader>
                <CardTitle>Temperature Comparison: 1990 vs 2024</CardTitle>
                <CardDescription>Interactive visualization showing temperature trends over time</CardDescription>
              </CardHeader>
              <CardContent className="p-0">
                <IframeVisualization />
              </CardContent>
            </Card>

            <div className="mt-8 grid gap-6 md:grid-cols-3">
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-base">How to Use</CardTitle>
                </CardHeader>
                <CardContent className="text-sm">
                  <ul className="list-disc pl-4 space-y-2">
                    <li>Use the buttons at the top to switch between visualization types</li>
                    <li>Hover over data points to see exact temperature values</li>
                    <li>Compare solid lines (2024) with dotted lines (1990) to observe changes</li>
                    <li>Toggle the different maximum, minimum, or average values on the legend to isolate them</li>
                  </ul>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-base">Key Findings</CardTitle>
                </CardHeader>
                <CardContent className="text-sm">
                  <ul className="list-disc pl-4 space-y-2">
                    <li>Maximum temperatures show significant increases during summer months</li>
                    <li>Minimum temperatures have risen more consistently throughout the year</li>
                    <li>The gap between 1990 and 2024 data illustrates the warming trend in Phoenix</li>
                  </ul>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-base">Data Sources</CardTitle>
                </CardHeader>
                <CardContent className="text-sm">
                  <p>
                    Temperature data was collected from NOAA Climate Data Online and the National Weather Service
                    Phoenix. All measurements are in Fahrenheit.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        {/* Resources Section */}
        <section id="resources" className="py-8 md:py-12 bg-slate-50">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center mb-8">
              <h2 className="text-3xl font-bold tracking-tighter">Resources</h2>
              <p className="max-w-[700px] text-muted-foreground">
                Explore these resources to learn more about climate change and Phoenix sustainability efforts.
              </p>
            </div>

            {/* Featured Video with Embedded YouTube */}
            <Card className="mb-8 overflow-hidden">
              <CardHeader>
                <CardTitle>How Climate Change is Affecting Phoenix's Neighborhoods</CardTitle>
                <CardDescription>
                  This video provides a scholarly overview of how climate change affects different types of
                  neighborhoods across Arizona and what we can do to implement change.
                </CardDescription>
              </CardHeader>
              <CardContent className="p-0">
                <div className="relative aspect-video">
                  {/* YouTube video embed */}
                  <iframe
                    src="https://www.youtube.com/embed/ZQ6fSHr5TJg?rel=0"
                    title="How Climate Change is Affecting Phoenix's Neighborhoods"
                    className="absolute inset-0 w-full h-full"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                    onLoad={() => setVideoLoaded(true)}
                    style={{
                      zIndex: 10,
                      backgroundColor: "transparent",
                    }}
                  ></iframe>

                  {/* Thumbnail image that shows before/behind the video */}
                  <div
                    className="absolute inset-0 bg-cover bg-center"
                    style={{
                      backgroundImage: `url('https://img.youtube.com/vi/ZQ6fSHr5TJg/maxresdefault.jpg')`,
                      backgroundSize: "cover",
                      opacity: videoLoaded ? 0 : 1,
                      transition: "opacity 0.5s ease",
                      zIndex: 5,
                    }}
                  ></div>
                </div>
              </CardContent>
            </Card>

            {/* Website Resources */}
            <h3 className="text-xl font-bold mb-4">Additional Resources</h3>
            <div className="grid gap-6 md:grid-cols-3">
              <ResourceCard
                title="NOAA Climate Data Online"
                description="Access historical climate data, tools, and resources from the National Oceanic and Atmospheric Administration."
                link="https://www.ncdc.noaa.gov/cdo-web/"
                bgColor="bg-blue-50"
                borderColor="border-blue-200"
                hoverColor="hover:bg-blue-100"
              />

              <ResourceCard
                title="National Weather Service Phoenix"
                description="Weather forecasts, warnings, and climate information specific to the Phoenix metropolitan area."
                link="https://www.weather.gov/psr/"
                bgColor="bg-green-50"
                borderColor="border-green-200"
                hoverColor="hover:bg-green-100"
              />

              <ResourceCard
                title="City of Phoenix Sustainability"
                description="Learn about Phoenix's sustainability initiatives, climate action plans, and environmental efforts."
                link="https://www.phoenix.gov/administration/departments/sustainability.html"
                bgColor="bg-purple-50"
                borderColor="border-purple-200"
                hoverColor="hover:bg-purple-100"
              />
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t bg-white">
        <div className="container flex flex-col gap-4 py-10 md:flex-row md:gap-8 md:py-8">
          <div className="flex flex-col gap-3 md:gap-2">
            <Link href="/" className="font-semibold">
              Phoenix Climate Data Visualization
            </Link>
            <p className="text-sm text-muted-foreground">Visualizing climate data to inform and educate.</p>
          </div>
          <div className="md:ml-auto flex flex-col md:flex-row gap-4 md:gap-8 text-sm">
            <Link href="#visualization" className="text-muted-foreground hover:text-foreground transition-colors">
              Visualization
            </Link>
            <Link href="#resources" className="text-muted-foreground hover:text-foreground transition-colors">
              Resources
            </Link>
          </div>
        </div>
        <div className="border-t py-6">
          <div className="container flex flex-col items-center justify-between gap-4 md:flex-row">
            <p className="text-center text-sm text-muted-foreground md:text-left">
              © 2024 Phoenix Climate Data Project. All rights reserved.
            </p>
            <p className="text-center text-sm text-muted-foreground md:text-left">Data updated: April 2024</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

// Resource Card Component with background color props
function ResourceCard({
  title,
  description,
  link,
  bgColor,
  borderColor,
  hoverColor,
}: {
  title: string
  description: string
  link: string
  bgColor: string
  borderColor: string
  hoverColor: string
}) {
  return (
    <Card className={`h-full flex flex-col ${bgColor} ${borderColor} transition-colors`}>
      <CardHeader className="pb-2">
        <CardTitle className="text-lg">{title}</CardTitle>
      </CardHeader>
      <CardContent className="flex-1">
        <p className="text-sm text-muted-foreground">{description}</p>
      </CardContent>
      <div className="p-6 pt-0 mt-auto">
        <Link
          href={link}
          target="_blank"
          rel="noopener noreferrer"
          className={`inline-flex items-center text-sm font-medium text-primary hover:underline px-3 py-2 rounded-md -mx-3 ${hoverColor}`}
        >
          Visit Website
          <ExternalLink className="ml-1 h-3 w-3" />
        </Link>
      </div>
    </Card>
  )
}
