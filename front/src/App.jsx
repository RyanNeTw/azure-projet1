import { useState } from "react";
import "./App.css";
import FormVote from "./components/FormVote";
import ListVote from "./components/ListVote";

function App() {
  return (
    <>
      <div>
        <h2 className="text-4xl italic font-bold">Byrou nous manque t-il ?</h2>
        <FormVote />
      </div>
      <div className="pt-4">
        <ListVote />
      </div>
    </>
  );
}

export default App;
