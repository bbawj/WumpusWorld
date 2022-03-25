:- abolish(current/3).
:- abolish(wumpus/2).
:- abolish(pit/2).
:- abolish(gold/2).
:- abolish(grab/2).
:- abolish(visited/2).
:- abolish(shooted/2).

:- dynamic([
  current/3,
  wumpus/2,
  pit/2,
  gold/2,
  grab/2,
  shooted/2,
  visited/2,
  is_bump/1
]).

% Defines the world NxM matrix.
world(7, 6).

% Initial player position
current(1, 1, east).
visited(1, 1).

% ---------------------------- %
% Environment predicates       %
% ---------------------------- %
has_gold(yes) :- grab(X, Y), gold(X, Y), !.
has_gold(no).

has_arrows(no) :- shooted(_, _), !.
has_arrows(yes).

% Perceptions
% ===========
% If has gold it has glitter.
has_glitter(yes) :- has_gold(G), G == no, current(X, Y, _), gold(X, Y), !.
has_glitter(no).

% Senses tingle if adjacent block has a pit.
has_tingle(yes) :-
  current(X, Y, _), N is Y + 1, pit(X, N), !;
  current(X, Y, _), S is Y - 1, pit(X, S), !;
  current(X, Y, _), E is X + 1, pit(E, Y), !;
  current(X, Y, _), W is X - 1, pit(W, Y), !.
has_tingle(no).

% Senses stench if adjacent block has the wumpus.
has_stench(yes) :-
  current(X, Y, _), N is Y + 1, wumpus(X, N), !;
  current(X, Y, _), S is Y - 1, wumpus(X, S), !;
  current(X, Y, _), E is X + 1, wumpus(E, Y), !;
  current(X, Y, _), W is X - 1, wumpus(W, Y), !.
has_stench(no).

% Senses bump if is facing a wall
has_bump(yes) :-
  world(W, _), current(W, _, east),  !;
  world(_, H), current(_, H, north), !;
  current(1, _, west),  !;
  current(_, 1, south), !.
has_bump(no).

is_bump(no).

% Senses screm if wumpus have died
has_scream(yes) :- is_wumpus(dead), !.
has_scream(no).

% Check player's condition
is_player(dead) :- current(X, Y, _), wumpus(X, Y), !.
is_player(dead) :- current(X, Y, _), pit(X, Y),    !.
is_player(alive).

% Check Wumpus condition
is_wumpus(dead) :- shooted(X, Y), wumpus(X, Y), !.
is_wumpus(alive).

% Check if position is into map bounds.
in_bounds(X, Y) :-
  world(W, H),
  X > 0, X =< W,
  Y > 0, Y =< H.

% Returns the current percetions
perceptions([Stench, Tingle, Glitter, Bump, Scream]) :-
  has_stench(Stench), has_tingle(Tingle), has_glitter(Glitter),
  is_bump(Bump), has_scream(Scream), !.

move(A, L) :-
  (
    A = shoot, shoot, !;
    A = moveforward, moveForward, !;
    A = turnleft, turnLeft, !;
    A = turnright, turnRight, !;
    A = pickup, pickup, !
  ),
  perceptions(L).

% Moves the Player to a new position.
moveForward :-
  has_bump(yes), retractall(is_bump(_)), asserta(is_bump(yes)), !.
moveForward :-
  retractall(is_bump(_)),
  asserta(is_bump(no)),
  (
    current(X,Y,D), D=east, Xi is X+1, Yi is Y, in_bounds(Xi, Yi), !;
    current(X,Y,D), D=west, Xi is X-1, Yi is Y, in_bounds(Xi, Y), !;
    current(X,Y,D), D=north, Xi is X, Yi is Y+1, in_bounds(X, Yi), !;
    current(X,Y,D), D=east, Xi is X, Yi is Y-1, in_bounds(X, Yi), !
    ),
    retractall(current(_,_,_)),
  asserta(current(Xi,Yi,D)).

turnLeft :- 
  (current(X, Y, D), D = east, ND = north, !;
  current(X, Y, D), D = north, ND = west, !;
  current(X, Y, D), D = west, ND = south, !;
  current(X, Y, D), D = south, ND = east, !),
  retractall(current(_,_,_)),
  asserta(current(X,Y,ND)).

turnRight :- 
  (current(X, Y, D), D = east, ND = south, !;
  current(X, Y, D), D = south, ND = west, !;
  current(X, Y, D), D = west, ND = north, !;
  current(X, Y, D), D = north, ND = east, !),
  retractall(current(_,_,_)),
  asserta(current(X,Y,ND)).

% Get the direction
direction(X, Y, D) :- current(Xi, Yi, _), X > Xi, Y == Yi, D = east,   !.
direction(X, Y, D) :- current(Xi, Yi, _), X == Xi, Y < Yi, D = north,  !.
direction(X, Y, D) :- current(Xi, Yi, _), X < Xi, Y == Yi, D = west,   !.
direction(X, Y, D) :- current(Xi, Yi, _), X == Xi, Y > Yi, D = south,  !.
direction(_, _, D) :- current(_, _, D).

% Shoot at given position
shoot :- has_arrows(no), write('!: I do not have arrows anymore.'), !.
shoot :-
  (
    current(X,Y,D), D=east, X is X+1, !;  
    current(X,Y,D), D=west, X is X-1, !;  
    current(X,Y,D), D=north, Y is Y+1, !;  
    current(X,Y,D), D=south, Y is Y-1, ! 
  ),
  has_arrows(yes),
  assertz(shooted(X, Y)).

% Get all adjacent blocks
neighbors(N) :- findall([X, Y], neighbors(X, Y), N).

% Define the adjacents blocks
neighbors(X, Y) :- current(Xi, Yi, _), E is Xi+1, in_bounds(E, Yi), X is E,  Y is Yi.
neighbors(X, Y) :- current(Xi, Yi, _), N is Yi+1, in_bounds(Xi, N), X is Xi, Y is N.
neighbors(X, Y) :- current(Xi, Yi, _), W is Xi-1, in_bounds(W, Yi), X is W,  Y is Yi.
neighbors(X, Y) :- current(Xi, Yi, _), S is Yi-1, in_bounds(Xi, S), X is Xi, Y is S.

% Player's actions
action(exit) :- write('Bye, bye!'), nl, print_result, nl, print_world, nl, halt.

action([move,  X, Y]) :- move(X, Y).
action([shoot, X, Y]) :- shoot(X, Y).

action(grab) :-
  assertz(actions(grab)),
  current(X, Y, _), assertz(grab(X, Y)),
  (gold(X, Y), has_gold(no)) ->
    write('!: Found gold! '), nl;
    true.