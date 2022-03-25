% Initial player position
hunter(1, 1, east).
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
has_glitter(yes) :- has_gold(G), G == no, hunter(X, Y, _), gold(X, Y), !.
has_glitter(no).

% Senses breeze if adjacent block has a pit.
has_breeze(yes) :-
  hunter(X, Y, _), N is Y + 1, pit(X, N), !;
  hunter(X, Y, _), S is Y - 1, pit(X, S), !;
  hunter(X, Y, _), E is X + 1, pit(E, Y), !;
  hunter(X, Y, _), W is X - 1, pit(W, Y), !.
has_breeze(no).

% Senses stench if adjacent block has the wumpus.
has_stench(yes) :-
  hunter(X, Y, _), N is Y + 1, wumpus(X, N), !;
  hunter(X, Y, _), S is Y - 1, wumpus(X, S), !;
  hunter(X, Y, _), E is X + 1, wumpus(E, Y), !;
  hunter(X, Y, _), W is X - 1, wumpus(W, Y), !.
has_stench(no).

% Senses bump if is facing a wall
has_bump(yes) :-
  world(W, _), hunter(W, _, east),  !;
  world(_, H), hunter(_, H, north), !;
  hunter(1, _, west),  !;
  hunter(_, 1, south), !.
has_bump(no).

% Senses screm if wumpus have died
has_scream(yes) :- is_wumpus(dead), !.
has_scream(no).

% Check player's condition
is_player(dead) :- hunter(X, Y, _), wumpus(X, Y), !.
is_player(dead) :- hunter(X, Y, _), pit(X, Y),    !.
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
perceptions([Stench, Breeze, Glitter, Bump, Scream]) :-
  has_stench(Stench), has_breeze(Breeze), has_glitter(Glitter),
  has_bump(Bump), has_scream(Scream), !.

% Moves the Player to a new position.
move(X, Y) :-
  assertz(actions(move)),
  in_bounds(X, Y),
  % format("- Moving to ~dx~d~n", [X, Y]),
  direction(X, Y, D),
  retractall(hunter(_, _, _)),
  asserta(hunter(X, Y, D)),
  assertz(visited(X, Y)),
  !.
move(X, Y) :- format('!: Cannot move to ~dx~d~n', [X, Y]).

% Get the direction
direction(X, Y, D) :- hunter(Xi, Yi, _), X > Xi, Y == Yi, D = east,   !.
direction(X, Y, D) :- hunter(Xi, Yi, _), X == Xi, Y < Yi, D = north,  !.
direction(X, Y, D) :- hunter(Xi, Yi, _), X < Xi, Y == Yi, D = west,   !.
direction(X, Y, D) :- hunter(Xi, Yi, _), X == Xi, Y > Yi, D = south,  !.
direction(_, _, D) :- hunter(_, _, D).

% Shoot at given position
shoot(_, _) :- has_arrows(no), write('!: I do not have arrows anymore.'), !.
shoot(X, Y) :-
  assertz(actions(shoot)),
  has_arrows(yes),
  assertz(shooted(X, Y)).

% Get all adjacent blocks
neighbors(N) :- findall([X, Y], neighbors(X, Y), N).

% Define the adjacents blocks
neighbors(X, Y) :- hunter(Xi, Yi, _), E is Xi+1, in_bounds(E, Yi), X is E,  Y is Yi.
neighbors(X, Y) :- hunter(Xi, Yi, _), N is Yi+1, in_bounds(Xi, N), X is Xi, Y is N.
neighbors(X, Y) :- hunter(Xi, Yi, _), W is Xi-1, in_bounds(W, Yi), X is W,  Y is Yi.
neighbors(X, Y) :- hunter(Xi, Yi, _), S is Yi-1, in_bounds(Xi, S), X is Xi, Y is S.

% Player's actions
action(exit) :- write('Bye, bye!'), nl, print_result, nl, print_world, nl, halt.

action([move,  X, Y]) :- move(X, Y).
action([shoot, X, Y]) :- shoot(X, Y).

action(grab) :-
  assertz(actions(grab)),
  hunter(X, Y, _), assertz(grab(X, Y)),
  (gold(X, Y), has_gold(no)) ->
    write('!: Found gold! '), nl;
    true.