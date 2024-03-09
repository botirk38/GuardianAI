import Head from 'next/head';
import Link from 'next/link';
import ReactSpeedometer from 'react-d3-speedometer'; // Make sure to install this package

export default function Home() {
  // Assume this accuracy value is dynamic and might be coming from props or state
  const accuracyPercentage = 75; // Replace with actual dynamic value as needed

  return (
    <div>
      <Head>
        <title>GuardianAI</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* Navbar with "MOTTO HERE" in the center */}
      <nav className="navbar z-50 px-6 lg:px-12 w-full" style={{ background: 'linear-gradient(to right, #0f2027, #203a43, #2c5364)', paddingTop: '30px' }}>
        <div className="flex justify-between items-center w-full">
          <div className="flex items-center">
            <Link href="/" className="btn btn-ghost normal-case text-lg lg:text-3xl font-extrabold text-black scale-200 hover:scale-125 transition-transform duration-300 ease-in-out px-0 flex items-center">
              <img alt="GuardianAI" src="lock.png" width="29" height="29" className="mr-2" />
              GuardianAI
            </Link>
          </div>
          <div className="italic" style={{ position: 'absolute', left: '50%', transform: 'translateX(-50%)' }}>
            "MOTTO HERE"
          </div>
          <div className="flex gap-4">
            <Link href="/login" className="btn btn-ghost text-black">Information</Link>
            <Link href="/get-started" className="btn text-black">Information1</Link>
          </div>
        </div>
      </nav>

      {/* Main content area with an "Analyze" button */}
      <main className="flex justify-center items-center h-screen" style={{ background: 'linear-gradient(to right, #0f2027, #203a43, #2c5364)' }}>
        <div className="flex w-full justify-center" style={{ padding: '20px' }}>
          {/* Left frame box */}
          <div className="bg-gray-800 rounded-lg shadow-lg" style={{ width: '550px', height: '500px', border: '10px solid black', marginRight: '30px' }}>
            {/* Speedometer component */}
            <div style={{ padding: '1rem' }}>
              <ReactSpeedometer
                maxValue={100}
                value={accuracyPercentage}
                needleColor="red"
                startColor="green"
                segments={10}
                endColor="red"
                textColor="white"
                height={400}
              />
            </div>
          </div>

          {/* Analyze button centered vertically */}
          <div className="my-auto" style={{ marginLeft: '30px', marginRight: '30px' }}>
            {/* ... existing button content ... */}
          </div>

          {/* Right frame box with textarea */}
          <div className="bg-gray-800 rounded-lg shadow-lg" style={{ width: '550px', height: '500px', border: '10px solid black', marginLeft: '30px' }}>
            {/* ... existing textarea content ... */}
          </div>
        </div>
      </main>
    </div>
  );
}