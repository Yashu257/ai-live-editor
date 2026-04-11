"""
FastAPI backend for React component generation.
Provides a simple endpoint to generate React components from user prompts.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Component Generator API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    """Request model for component generation."""
    prompt: str


class GenerateResponse(BaseModel):
    """Response model containing generated component code."""
    component: str
    code: str
    success: bool
    message: str = ""


def generate_component_code(prompt: str) -> tuple[str, str]:
    """
    Generate a React component based on the user prompt.

    Detects which component to target:
    - "login" → Hero.jsx (with login form content)
    - "navbar" → Navbar.jsx
    - "footer" → Footer.jsx
    - default → Hero.jsx

    Returns: (component_name, component_code)
    """
    prompt_lower = prompt.lower()

    if "login" in prompt_lower:
        # Return login form as Hero component
        return ("Hero.jsx", _generate_login_form(prompt))
    elif "navbar" in prompt_lower:
        return ("Navbar.jsx", _generate_navbar_component(prompt))
    elif "footer" in prompt_lower:
        return ("Footer.jsx", _generate_footer_component(prompt))
    else:
        # Default to Hero.jsx for any other prompt
        return ("Hero.jsx", _generate_hero_component(prompt))


def _generate_hero_component(prompt: str) -> str:
    """Generate a hero section component (default fallback)."""
    return f"""import React from 'react';

// Generated hero component based on: {prompt}
export default function Hero() {{
  return (
    <section className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-16">
      <div className="max-w-7xl mx-auto px-4 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          Generated Hero
        </h1>
        <p className="text-xl text-blue-100">
          Prompt: {prompt}
        </p>
      </div>
    </section>
  );
}}"""


def _generate_navbar_component(prompt: str) -> str:
    """Generate a navbar component."""
    return f"""import React from 'react';

// Generated navbar component based on: {prompt}
export default function Navbar() {{
  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <span className="text-xl font-bold text-blue-600">GeneratedNav</span>
          <div className="space-x-4">
            <a href="#" className="text-gray-600 hover:text-blue-600">Home</a>
            <a href="#" className="text-gray-600 hover:text-blue-600">About</a>
            <a href="#" className="text-gray-600 hover:text-blue-600">Contact</a>
          </div>
        </div>
      </div>
    </nav>
  );
}}"""


def _generate_footer_component(prompt: str) -> str:
    """Generate a footer component."""
    return f"""import React from 'react';

// Generated footer component based on: {prompt}
export default function Footer() {{
  return (
    <footer className="bg-gray-800 text-gray-300 py-6">
      <div className="max-w-7xl mx-auto px-4 text-center">
        <p className="text-sm">Generated Footer - {{prompt}}</p>
      </div>
    </footer>
  );
}}"""


def _generate_login_form(prompt: str) -> str:
    """Generate a login form component (exported as Hero for Hero.jsx slot)."""
    return f"""import React, {{ useState }} from 'react';

// Generated login form for Hero section based on: {prompt}
export default function Hero() {{
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {{
    e.preventDefault();
    console.log('Login:', {{ email, password }});
  }};

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form onSubmit={{handleSubmit}} className="w-full max-w-md p-8 bg-white rounded-xl shadow-lg">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">Login</h2>

        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-medium mb-2">Email</label>
          <input
            type="email"
            value={{email}}
            onChange={{(e) => setEmail(e.target.value)}}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your email"
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-gray-700 text-sm font-medium mb-2">Password</label>
          <input
            type="password"
            value={{password}}
            onChange={{(e) => setPassword(e.target.value)}}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your password"
            required
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white font-semibold py-3 rounded-lg hover:bg-blue-700 transition-colors"
        >
          Sign In
        </button>

        <p className="mt-4 text-center text-gray-600 text-sm">
          Don't have an account? <a href="#" className="text-blue-600 hover:underline">Sign up</a>
        </p>
      </form>
    </div>
  );
}}"""


def _generate_signup_form(prompt: str) -> str:
    """Generate a signup form component."""
    return f"""import React, {{ useState }} from 'react';

// Generated signup form based on: {prompt}
export default function SignupForm() {{
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = (e) => {{
    e.preventDefault();
    console.log('Signup:', {{ name, email, password }});
  }};

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form onSubmit={{handleSubmit}} className="w-full max-w-md p-8 bg-white rounded-xl shadow-lg">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">Sign Up</h2>

        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-medium mb-2">Full Name</label>
          <input
            type="text"
            value={{name}}
            onChange={{(e) => setName(e.target.value)}}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your name"
            required
          />
        </div>

        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-medium mb-2">Email</label>
          <input
            type="email"
            value={{email}}
            onChange={{(e) => setEmail(e.target.value)}}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your email"
            required
          />
        </div>

        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-medium mb-2">Password</label>
          <input
            type="password"
            value={{password}}
            onChange={{(e) => setPassword(e.target.value)}}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="Create a password"
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-gray-700 text-sm font-medium mb-2">Confirm Password</label>
          <input
            type="password"
            value={{confirmPassword}}
            onChange={{(e) => setConfirmPassword(e.target.value)}}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="Confirm your password"
            required
          />
        </div>

        <button
          type="submit"
          className="w-full bg-green-600 text-white font-semibold py-3 rounded-lg hover:bg-green-700 transition-colors"
        >
          Create Account
        </button>

        <p className="mt-4 text-center text-gray-600 text-sm">
          Already have an account? <a href="#" className="text-blue-600 hover:underline">Login</a>
        </p>
      </form>
    </div>
  );
}}"""


def _generate_contact_form(prompt: str) -> str:
    """Generate a contact form component."""
    return f"""import React, {{ useState }} from 'react';

// Generated contact form based on: {prompt}
export default function ContactForm() {{
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {{
    e.preventDefault();
    console.log('Contact form:', {{ name, email, message }});
  }};

  return (
    <div className="max-w-lg mx-auto p-8 bg-white rounded-xl shadow-md">
      <h2 className="text-2xl font-bold text-gray-800 mb-2 text-center">Contact Us</h2>
      <p className="text-gray-600 text-center mb-6">We'd love to hear from you!</p>

      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-medium mb-2">Name</label>
        <input
          type="text"
          value={{name}}
          onChange={{(e) => setName(e.target.value)}}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          placeholder="Your name"
          required
        />
      </div>

      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-medium mb-2">Email</label>
        <input
          type="email"
          value={{email}}
          onChange={{(e) => setEmail(e.target.value)}}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          placeholder="your@email.com"
          required
        />
      </div>

      <div className="mb-6">
        <label className="block text-gray-700 text-sm font-medium mb-2">Message</label>
        <textarea
          value={{message}}
          onChange={{(e) => setMessage(e.target.value)}}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg h-32 resize-none focus:ring-2 focus:ring-blue-500"
          placeholder="Your message..."
          required
        />
      </div>

      <button
        type="submit"
        onClick={{handleSubmit}}
        className="w-full bg-blue-600 text-white font-semibold py-3 rounded-lg hover:bg-blue-700 transition-colors"
      >
        Send Message
      </button>
    </div>
  );
}}"""


@app.post("/generate", response_model=GenerateResponse)
async def generate_component(request: GenerateRequest) -> GenerateResponse:
    """
    Generate a React component based on the provided prompt.
    
    Args:
        request: GenerateRequest containing the user prompt
        
    Returns:
        GenerateResponse with the generated code or error message
    """
    try:
        if not request.prompt.strip():
            return GenerateResponse(
                component="",
                code="",
                success=False,
                message="Prompt cannot be empty"
            )
        
        component_name, code = generate_component_code(request.prompt)

        return GenerateResponse(
            component=component_name,
            code=code,
            success=True,
            message="Component generated successfully"
        )
    except Exception as e:
        return GenerateResponse(
            component="",
            code="",
            success=False,
            message=f"Error generating component: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
