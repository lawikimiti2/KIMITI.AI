import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Brain, FileText, MessageSquare, Sparkles, Upload, Zap } from "lucide-react";
import { Link } from "react-router-dom";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Brain className="w-8 h-8 text-primary" />
            <h1 className="text-2xl font-bold text-foreground">Kimiti AI</h1>
          </div>
          <nav className="flex items-center gap-4">
            <Link to="/chat">
              <Button variant="ghost">Chat</Button>
            </Link>
            <Link to="/documents">
              <Button variant="ghost">Documents</Button>
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero Content */}
      <section className="container mx-auto px-4 py-20 text-center">
        <div className="max-w-4xl mx-auto space-y-8">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium mb-4">
            <Sparkles className="w-4 h-4" />
            Powered by Advanced AI
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold text-foreground leading-tight">
            Your Intelligent Assistant for
            <span className="text-primary"> Tendering & Business</span>
          </h1>
          
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Streamline tender processing, generate professional proposals, and automate your business operations with AI-powered intelligence.
          </p>

          <div className="flex items-center justify-center gap-4 pt-4">
            <Link to="/chat">
              <Button size="lg" className="gap-2">
                <MessageSquare className="w-5 h-5" />
                Start Chat
              </Button>
            </Link>
            <Link to="/documents">
              <Button size="lg" variant="outline" className="gap-2">
                <Upload className="w-5 h-5" />
                Upload Documents
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center mb-12 text-foreground">Key Features</h2>
        
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <Card className="border-border hover:shadow-lg transition-shadow">
            <CardHeader>
              <FileText className="w-12 h-12 text-primary mb-4" />
              <CardTitle>Tender Processing</CardTitle>
              <CardDescription>
                Automatically extract requirements, BOQ, eligibility criteria, and compliance checklists from tender documents
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-border hover:shadow-lg transition-shadow">
            <CardHeader>
              <MessageSquare className="w-12 h-12 text-primary mb-4" />
              <CardTitle>AI Chat Assistant</CardTitle>
              <CardDescription>
                Get intelligent support for business operations, technical queries, and proposal generation with context-aware responses
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-border hover:shadow-lg transition-shadow">
            <CardHeader>
              <Zap className="w-12 h-12 text-primary mb-4" />
              <CardTitle>Document Generation</CardTitle>
              <CardDescription>
                Generate technical proposals, work plans, BOQ costing, and financial documents with AI assistance
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-16">
        <Card className="bg-gradient-to-br from-primary/10 to-accent/5 border-primary/20">
          <CardContent className="p-12 text-center">
            <h2 className="text-3xl font-bold mb-4 text-foreground">Ready to Transform Your Workflow?</h2>
            <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
              Start using Kimiti AI today to automate tender processing and boost your business efficiency
            </p>
            <Link to="/chat">
              <Button size="lg" className="gap-2">
                <Brain className="w-5 h-5" />
                Get Started Now
              </Button>
            </Link>
          </CardContent>
        </Card>
      </section>

      {/* Footer */}
      <footer className="border-t border-border mt-20">
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Brain className="w-6 h-6 text-primary" />
              <span className="font-semibold text-foreground">Kimiti AI</span>
            </div>
            <p className="text-sm text-muted-foreground">
              © 2024 Kimiti AI. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
