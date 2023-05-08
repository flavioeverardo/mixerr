%#const tracks = 2.

%% Number of tracks... given by the constant above
track(1..tracks).

%% The range of decibels to pick
%decibel(-40..0).

%% Select a decibel to each track
1 { track_decibel(T,DB) : decibel(DB) } 1 :- track(T).

%% Convert dB to linear amplitude
track_amplitude(T, @db2linear(DB)) :- track_decibel(T,DB).

%% Check that linear amplitude fits in the range of -3 to 0 dBFS
:- 95 < #sum{A,T : track_amplitude(T,A)}. %% Max  0 dBFS
:-  70 > #sum{A,T : track_amplitude(T,A)}. %% Min -3 dBFS

#show track_decibel/2.
