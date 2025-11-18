import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Brain, Upload, FileText, File } from "lucide-react";
import { Link } from "react-router-dom";

const Documents = () => {
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      // Handle file upload - will be implemented with backend
      console.log("File dropped:", e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <Brain className="w-8 h-8 text-primary" />
            <h1 className="text-2xl font-bold text-foreground">Kimiti AI</h1>
          </Link>
          <Link to="/chat">
            <Button variant="outline">Go to Chat</Button>
          </Link>
        </div>
      </header>

      {/* Upload Section */}
      <div className="container mx-auto px-4 py-12 max-w-4xl">
        <h2 className="text-3xl font-bold mb-8 text-foreground">Document Processing</h2>
        
        <Card
          className={`p-12 border-2 border-dashed transition-colors ${
            dragActive ? "border-primary bg-primary/5" : "border-border"
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <div className="flex flex-col items-center justify-center text-center space-y-4">
            <Upload className="w-16 h-16 text-muted-foreground" />
            <div>
              <p className="text-xl font-semibold text-foreground mb-2">
                Upload Tender Documents
              </p>
              <p className="text-muted-foreground">
                Drag and drop files here or click to browse
              </p>
              <p className="text-sm text-muted-foreground mt-2">
                Supported formats: PDF, Word, Excel
              </p>
            </div>
            <Button>
              <File className="w-4 h-4 mr-2" />
              Select Files
            </Button>
          </div>
        </Card>

        {/* Features List */}
        <div className="mt-12 grid md:grid-cols-2 gap-6">
          <Card className="p-6 bg-card border-border">
            <FileText className="w-10 h-10 text-primary mb-3" />
            <h3 className="text-lg font-semibold mb-2 text-card-foreground">Automatic Extraction</h3>
            <p className="text-muted-foreground">
              Extract requirements, BOQ, eligibility criteria, and compliance checklists automatically
            </p>
          </Card>

          <Card className="p-6 bg-card border-border">
            <Brain className="w-10 h-10 text-primary mb-3" />
            <h3 className="text-lg font-semibold mb-2 text-card-foreground">AI Analysis</h3>
            <p className="text-muted-foreground">
              Generate summaries, identify key points, and provide intelligent insights
            </p>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Documents;
