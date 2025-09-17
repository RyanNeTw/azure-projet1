import { useForm } from "react-hook-form";

const FormVote = () => {
  const inputStyle = `border rounded px-2 py-1`;

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm();

  const onSubmit = async (data) => {
    await fetch("https://bayrou-functions.azurewebsites.net/api/postvote", {
      method: "POST",
      body: JSON.stringify(data),
    });
  };

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-2">
        <input
          placeholder="email@google.com"
          {...register("email", { required: true })}
          className={`${inputStyle} ${
            errors.email ? "border-red-600" : "border-white"
          }`}
        />

        <input
          placeholder={"Pseudo"}
          {...register("pseudo", { required: true })}
          className={`${inputStyle} ${
            errors.pseudo ? "border-red-600" : "border-white"
          }`}
        />

        <div className="flex flex-row justify-center gap-2">
          <span>Vote</span>
          <input type="checkbox" defaultChecked={false} {...register("vote")} />
        </div>

        <input
          type="submit"
          className="border border-white rounded py-2 transition hover:bg-white hover:text-black"
        />
      </form>
    </>
  );
};

export default FormVote;
