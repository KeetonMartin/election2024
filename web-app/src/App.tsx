import { useEffect, useState } from "react"
import { CartesianGrid, XAxis, Bar, BarChart, ResponsiveContainer, Tooltip, Legend } from "recharts"
import { ThemeProvider } from "./components/theme-provider"
import { ChartContainer, ChartTooltip, ChartTooltipContent, ChartLegendContent } from "./components/ui/chart"

interface SimulationResult {
  timestamp: string
  win_probabilities: {
    "Donald Trump": number
    "Kamala Harris": number
  }
}

const chartConfig = {
  "Donald Trump": {
    label: "Donald Trump",
    color: "hsl(0, 100%, 50%)", // Bright red
  },
  "Kamala Harris": {
    label: "Kamala Harris",
    color: "hsl(240, 100%, 50%)", // Bright blue
  },
} satisfies ChartConfig

function App() {
  const [chartData, setChartData] = useState<SimulationResult[]>([])

  useEffect(() => {
    fetch('/simulation_results.json')
      .then(response => response.json())
      .then(data => setChartData(data))
      .catch(error => console.error('Error fetching data:', error))
  }, [])

  const formattedData = chartData.map(result => ({
    timestamp: new Date(result.timestamp).getTime(),
    "Donald Trump": result.win_probabilities["Donald Trump"] * 100,
    "Kamala Harris": result.win_probabilities["Kamala Harris"] * 100,
  }))

  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <div className="min-h-screen w-full flex flex-col items-center">
        <header className="sticky top-0 flex h-16 items-center gap-4 border-b bg-background px-4 w-full">
          <h1 className="text-2xl font-bold">Election Dashboard</h1>
        </header>
        <main className="flex-1 space-y-4 p-8 pt-6 w-full max-w-6xl">
          <div className="flex justify-center">
            <ChartContainer config={chartConfig} className="h-[70vh] w-full max-w-4xl">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={formattedData}>
                  <CartesianGrid vertical={false} />
                  <XAxis
                    dataKey="timestamp"
                    tickLine={false}
                    tickMargin={10}
                    axisLine={false}
                    tickFormatter={(value) => new Date(value).toLocaleDateString()}
                  />
                  <Tooltip content={<ChartTooltipContent />} />
                  <Legend content={<ChartLegendContent />} />
                  <Bar dataKey="Donald Trump" fill={chartConfig["Donald Trump"].color} radius={4} />
                  <Bar dataKey="Kamala Harris" fill={chartConfig["Kamala Harris"].color} radius={4} />
                </BarChart>
              </ResponsiveContainer>
            </ChartContainer>
          </div>
        </main>
      </div>
    </ThemeProvider>
  )
}

export default App