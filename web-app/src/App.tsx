import { useEffect, useState } from "react"
import { TrendingUp, Users, DollarSign } from "lucide-react"
import {
  CartesianGrid,
  Line,
  LineChart,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Tooltip,
  Area,
  AreaChart,
  Bar,
  BarChart,
  PolarAngleAxis,
  RadialBar,
  RadialBarChart,
} from "recharts"

import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "./components/ui/card"
import { ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent } from "./components/ui/chart"
import { Separator } from "./components/ui/separator"
import { ThemeProvider } from "./components/theme-provider"
import { Button } from "./components/ui/button"
import { Menu } from "lucide-react"
import { Sheet, SheetContent, SheetTrigger } from "./components/ui/sheet"

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
      <div className="flex min-h-screen w-full flex-col">
        <header className="sticky top-0 flex h-16 items-center gap-4 border-b bg-background px-4 md:px-6">
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="outline" size="icon" className="shrink-0 md:hidden">
                <Menu className="h-5 w-5" />
                <span className="sr-only">Toggle navigation menu</span>
              </Button>
            </SheetTrigger>
            <SheetContent side="left">
              <nav className="grid gap-6 text-lg font-medium">
                <a href="#" className="hover:text-foreground">Dashboard</a>
                <a href="#" className="hover:text-foreground">Analytics</a>
              </nav>
            </SheetContent>
          </Sheet>
          <nav className="hidden md:flex items-center space-x-4">
            <a href="#" className="text-sm font-medium hover:text-foreground">Dashboard</a>
            <a href="#" className="text-sm font-medium hover:text-foreground">Analytics</a>
          </nav>
        </header>
        <main className="flex-1 space-y-4 p-8 pt-6">
          <div className="flex items-center justify-between space-y-2">
            <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
          </div>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card className="lg:max-w-md">
              <CardHeader className="space-y-0 pb-2">
                <CardDescription>Win Probability</CardDescription>
                <CardTitle className="text-4xl tabular-nums">
                  {formattedData[formattedData.length - 1]?.["Donald Trump"].toFixed(2)}%
                  <span className="font-sans text-sm font-normal tracking-normal text-muted-foreground"> Trump</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ChartContainer config={chartConfig}>
                  <ResponsiveContainer width="100%" height={350}>
                    <LineChart data={formattedData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis
                        dataKey="timestamp"
                        type="number"
                        domain={['dataMin', 'dataMax']}
                        tickFormatter={(unixTime) => new Date(unixTime).toLocaleDateString()}
                        stroke="#888888"
                      />
                      <YAxis
                        domain={[40, 60]}
                        tickFormatter={(value) => `${value}%`}
                        stroke="#888888"
                      />
                      <Tooltip
                        formatter={(value: number) => [`${value.toFixed(2)}%`, '']}
                        labelFormatter={(label) => new Date(label).toLocaleString()}
                      />
                      <Line
                        type="monotone"
                        dataKey="Donald Trump"
                        stroke={chartConfig["Donald Trump"].color}
                        strokeWidth={2}
                        dot={false}
                      />
                      <Line
                        type="monotone"
                        dataKey="Kamala Harris"
                        stroke={chartConfig["Kamala Harris"].color}
                        strokeWidth={2}
                        dot={false}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </ChartContainer>
              </CardContent>
            </Card>
            <Card className="flex flex-col lg:max-w-md">
              <CardHeader className="flex flex-row items-center gap-4 space-y-0 pb-2 [&>div]:flex-1">
                <div>
                  <CardDescription>Trump's Avg</CardDescription>
                  <CardTitle className="flex items-baseline gap-1 text-4xl tabular-nums">
                    {(formattedData.reduce((sum, data) => sum + data["Donald Trump"], 0) / formattedData.length).toFixed(2)}
                    <span className="text-sm font-normal tracking-normal text-muted-foreground">%</span>
                  </CardTitle>
                </div>
                <div>
                  <CardDescription>Harris' Avg</CardDescription>
                  <CardTitle className="flex items-baseline gap-1 text-4xl tabular-nums">
                    {(formattedData.reduce((sum, data) => sum + data["Kamala Harris"], 0) / formattedData.length).toFixed(2)}
                    <span className="text-sm font-normal tracking-normal text-muted-foreground">%</span>
                  </CardTitle>
                </div>
              </CardHeader>
              <CardContent className="flex flex-1 items-center">
                <ChartContainer config={chartConfig} className="w-full">
                  <AreaChart data={formattedData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="timestamp" type="number" tickFormatter={(unixTime) => new Date(unixTime).toLocaleDateString()} />
                    <YAxis domain={[40, 60]} />
                    <Tooltip formatter={(value: number) => [`${value.toFixed(2)}%`, '']} labelFormatter={(label) => new Date(label).toLocaleString()} />
                    <Area type="monotone" dataKey="Donald Trump" stackId="1" stroke={chartConfig["Donald Trump"].color} fill={chartConfig["Donald Trump"].color} />
                    <Area type="monotone" dataKey="Kamala Harris" stackId="1" stroke={chartConfig["Kamala Harris"].color} fill={chartConfig["Kamala Harris"].color} />
                  </AreaChart>
                </ChartContainer>
              </CardContent>
            </Card>
          </div>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
            <Card className="col-span-4">
              <CardHeader>
                <CardTitle>Comparison</CardTitle>
                <CardDescription>Trump vs Harris win probability</CardDescription>
              </CardHeader>
              <CardContent className="grid gap-4">
                <ChartContainer config={chartConfig} className="h-[140px] w-full">
                  <BarChart
                    layout="vertical"
                    data={[
                      { name: "Trump", value: formattedData[formattedData.length - 1]?.["Donald Trump"] },
                      { name: "Harris", value: formattedData[formattedData.length - 1]?.["Kamala Harris"] },
                    ]}
                  >
                    <XAxis type="number" />
                    <YAxis dataKey="name" type="category" />
                    <Bar dataKey="value" fill={chartConfig["Donald Trump"].color} />
                  </BarChart>
                </ChartContainer>
              </CardContent>
            </Card>
            <Card className="col-span-3">
              <CardContent className="flex gap-4 p-4">
                <ChartContainer config={chartConfig} className="mx-auto aspect-square w-full max-w-[80%]">
                  <RadialBarChart
                    innerRadius="20%"
                    outerRadius="100%"
                    data={[
                      { name: "Trump", value: formattedData[formattedData.length - 1]?.["Donald Trump"] },
                      { name: "Harris", value: formattedData[formattedData.length - 1]?.["Kamala Harris"] },
                    ]}
                    startAngle={0}
                    endAngle={360}
                  >
                    <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />
                    <RadialBar background dataKey="value" />
                  </RadialBarChart>
                </ChartContainer>
              </CardContent>
            </Card>
          </div>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <StatsCard title="Total Simulations" value="1,000" icon={BarChart} change="+20.1%" />
            <StatsCard title="Avg. Confidence" value="85.2%" icon={Users} change="+180.1%" />
            <StatsCard title="Data Points" value="12,234" icon={DollarSign} change="+19%" />
            <StatsCard title="Active Models" value="3" icon={TrendingUp} change="+201" />
          </div>
        </main>
      </div>
    </ThemeProvider>
  )
}

function StatsCard({ title, value, icon: Icon, change }: { title: string, value: string, icon: React.ElementType, change: string }) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <Icon className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <p className="text-xs text-muted-foreground">{change} from last month</p>
      </CardContent>
    </Card>
  )
}

function Overview() {
  return (
    <div className="space-y-4">
      <h3 className="scroll-m-20 text-2xl font-semibold tracking-tight">
        Election Simulation Insights
      </h3>
      <p className="leading-7">
        Our advanced election simulation model provides a comprehensive analysis of the 2024 presidential race, 
        focusing on the potential outcomes for candidates Donald Trump and Kamala Harris.
      </p>
      <h4 className="scroll-m-20 text-xl font-semibold tracking-tight">
        Key Findings
      </h4>
      <ul className="my-6 ml-6 list-disc [&>li]:mt-2">
        <li>Tight race with fluctuating lead</li>
        <li>Significant impact of recent political events</li>
        <li>Swing states playing a crucial role</li>
      </ul>
      <p className="leading-7">
        The simulation results demonstrate the dynamic nature of the election, with win probabilities 
        shifting based on various factors including polling data, economic indicators, and campaign strategies.
      </p>
      <blockquote className="mt-6 border-l-2 pl-6 italic">
        "In this election, every percentage point counts. The race remains incredibly close, 
        highlighting the importance of voter turnout and last-minute campaign efforts."
      </blockquote>
    </div>
  )
}

export default App