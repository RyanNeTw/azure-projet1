import { useEffect, useState } from "react";

const ListVote = () => {
  const [votes, setVotes] = useState([]);

  const getVotes = async () => {
    try {
      const res = await fetch(
        "https://bayrou-functions.azurewebsites.net/api/getvotes"
      );

      if (!res.ok) {
        throw new Error(`Erreur API: ${res.status}`);
      }

      const response = await res.json();
      console.log(response.data);
      setVotes(response.data);
      console.log(votes);
    } catch (err) {
      console.error("Erreur lors du fetch votes:", err);
    }
  };

  useEffect(() => {
    getVotes();
  }, []);

  return (
    <>
      <ul className="flex flex-col gap-2">
        <button onClick={getVotes} className="bg-white rounded text-white">
          Refresh
        </button>
        <div className="flex flex-row justify-center gap-2">
          <span className="bg-white text-black px-4 py-2 rounded">
            {votes?.length}
          </span>
          <span className="bg-green-600 text-white px-4 py-2 rounded">
            {
              votes?.filter((v) => {
                return v?.data?.vote;
              })?.length
            }
          </span>
          <span className="bg-red-600 text-white px-4 py-2 rounded">
            {
              votes?.filter((v) => {
                return !v?.data?.vote;
              })?.length
            }
          </span>
        </div>
        {votes?.map((vote) => (
          <li key={vote.data.id}>
            <p
              className={
                vote.data.vote ? "bg-green-600" : "bg-red-600" + " rounded"
              }
            >
              {vote.data.user_id}
            </p>
          </li>
        ))}
      </ul>
    </>
  );
};

export default ListVote;
