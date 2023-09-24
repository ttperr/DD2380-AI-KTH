# HMM Labs

> Done by Tristan PERROT & Étienne RIGUET

## Questions

> **Question 1** This problem can be formulated in matrix form. Please specify the initial probability vector π, the transition probability matrix A and the observation probability matrix B

$$
\pi = \begin{bmatrix} 0.5 \\ 0.5 \end{bmatrix} ;
A = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix};
B = \begin{bmatrix} 0.9 & 0.1 \\ 0.5 & 0.5 \end{bmatrix}
$$

> **Question 2** What is the result of this operation?

$$
\pi \times A = \begin{bmatrix} 0.5 \\ 0.5 \end{bmatrix} \times \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 0.5 & 0.5 \end{bmatrix}
$$

> **Question 3** What is the result of this operation?

$$
\pi \times A \times B = \begin{bmatrix} 0.5 \\ 0.5 \end{bmatrix} \times \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \times \begin{bmatrix} 0.9 & 0.1 \\ 0.5 & 0.5 \end{bmatrix} = \begin{bmatrix} 0.7 \\ 0.3 \end{bmatrix}
$$

> **Question 4** Why is it valid to substitute O1:t =o1:t with Ot =ot when we condition on the state Xt =xi ?

Because the observations are independent from each other, so the probability of observing the sequence O1:t =o1:t is the same as the probability of observing the sequence Ot =ot.

> **Question 5** How many values are stored in the matrices δ and δ^idx respectively?

*Answer*

> **Question 6** Why we do we need to divide by the sum over the final α values for the di-gamma function?

*Answer*

> **Question 7** Train an HMM with the same parameter dimensions as above, i.e. A should be a 3 times 3 matrix, etc. Initialize your algorithm with the following matrices: A = [0.54 0.26 0.2; 0.19 0.53 0.28; 0.22 0.18 0.6], B = [0.5 0.2 0.11 0.19; 0.22 0.28 0.23 0.27; 0.19 0.21 0.15 0.45], π = [0.3; 0.2; 0.5]. Use the same data as in the previous question. Run the Baum-Welch algorithm for 10 iterations. What are the final values of A, B and π?

*Answer*

> **Question 8** Train an HMMwith the same parameter dimensions as above, i.e. A is a 3x3 matrix etc. The initialization is left up to you.
> How close do you get to the parameters above, i.e. how close do you get to the generating parameters in Eq. 3.1? What is the problem when it comes to estimating the distance between these matrices? How can you solve these issues?

*Answer*

> **Question 9** Train an HMM with different numbers of hidden states.
> What happens if you use more or less than 3 hidden states? Why? Are three hidden states and four observations the best choice? If not, why? How can you deter-
mine the optimal setting? How does this depend on the amount of data you have?

*Answer*

> **Question 10** Initialize your Baum-Welch algorithm with a uniform distribution. How does this affect the learning?
> Initialize your Baum-Welch algorithm with a diagonal A matrix and π = [0,0,1]. How does this affect the learning?
> Initialize your Baum-Welch algorithm with a matrices that are close to the solution. How does this affect the learning?

*Answer*
