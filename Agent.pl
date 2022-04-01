:- abolish(current/2).
:- abolish(wumpus/2).
:- abolish(stench/1).
:- abolish(pit/2).
:- abolish(gold/2).
:- abolish(grab/2).
:- abolish(visited/1).
:- abolish(shooted/2).
:- abolish(wall/1).

:- dynamic([
  current/2,
  wumpus/2,
  stench/1,
  pit/2,
  gold/2,
  grab/2,
  shooted/2,
  visited/1,
  is_bump/1,
  wall/1
]).

% Defines the world NxM matrix.
world(7, 6).
gold(2,3).
wumpus(1,3).

% Initial player position
current(r(1, 1), north).
visited(r(1, 1)).

% ---------------------------- %
% Environment predicates       %
% ---------------------------- %
visited(X,Y) :- visited(r(X,Y)).
current(X,Y,D) :- current(r(X,Y),D).

has_gold(yes) :- grab(X, Y), gold(X, Y), !.
has_gold(no).

has_arrows(no) :- shooted(_, _), !.
has_arrows(yes).

% Perceptions
% ===========
% If has gold it has glitter.
% has_glitter(yes) :- has_gold(G), G == no, current(X, Y, _), gold(X, Y), !.
has_glitter(no).

% Senses tingle if adjacent block has a pit.
% has_tingle(yes) :-
%   current(r(X, Y), _), N is Y + 1, pit(X, N), !;
%   current(X, Y, _), S is Y - 1, pit(X, S), !;
%   current(X, Y, _), E is X + 1, pit(E, Y), !;
%   current(X, Y, _), W is X - 1, pit(W, Y), !.
has_tingle(no).

% Senses stench if adjacent block has the wumpus.
has_stench(yes) :-
  current(r(X,Y), _),
  ((N is Y + 1, wumpus(X, N));
  (S is Y - 1, wumpus(X, S));
  (E is X + 1, wumpus(E, Y));
  (W is X - 1, wumpus(W, Y))),
  add_stench_kb(X,Y).
has_stench(no).

add_stench_kb(X,Y):-
  \+ stench(r(X,Y)) -> assertz(stench(r(X,Y))) ; true.

% Senses bump if is facing a wall
has_bump(yes) :-
  world(W,H),
  (current(r(W-1, _), east);
  current(r(_, H-1), north);
  current(r(1, _), west);
  current(r(_, 1), south)).
has_bump(no).

add_wall_kb(X,Y,D):-
  getForwardRoom(r(X,Y),D,N),
  \+ wall(N) -> assertz(wall(N)) ; true.

is_bump(no).

% Senses screm if wumpus have died
has_scream(yes) :- is_wumpus(dead), !.
has_scream(no).

% Check player's condition
is_player(dead) :- current(r(X, Y), _), wumpus(X, Y), !.
% is_player(dead) :- current(X, Y, _), pit(X, Y),    !.
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
    A = shoot -> shoot ;
    A = moveforward -> moveForward  ;
    A = turnleft -> turnLeft ;
    A = turnright -> turnRight ;
    A = pickup -> pickup
  ),
  perceptions(L).

% Moves the Player to a new position.
moveForward :-
  has_bump(yes), retractall(is_bump(_)), asserta(is_bump(yes)), current(r(X,Y),D), add_wall_kb(X,Y,D).
moveForward :-
  retractall(is_bump(_)),
  asserta(is_bump(no)),
  current(r(X,Y),D),
  getForwardRoom(r(X,Y),D, N),
  retractall(current(_,_)),
  assertz(visited(N)),
  asserta(current(N,D)).

turnLeft :- 
  current(r(X,Y),D),
  (D = east, ND = north, !;
   D = north, ND = west, !;
   D = west, ND = south, !;
   D = south, ND = east, !),
  retractall(current(_,_)),
  asserta(current(r(X,Y),ND)).

turnRight :- 
  current(r(X,Y),D),
  (
    (D = east, ND = south);
    (D = south, ND = west);
    (D = west, ND = north);
    (D = north, ND = east)),
  retractall(current(_,_)),
  asserta(current(r(X,Y),ND)).

% Shoot at given position
% shoot :- has_arrows(no), write('!: I do not have arrows anymore.'), !.
% shoot :-
%   (
%     current(X,Y,D), D=east, X is X+1, !;  
%     current(X,Y,D), D=west, X is X-1, !;  
%     current(X,Y,D), D=north, Y is Y+1, !;  
%     current(X,Y,D), D=south, Y is Y-1, ! 
%   ),
%   has_arrows(yes),
%   assertz(shooted(X, Y)).

% Evaluates possibility of Wumpus in a certain room. Checks if all
% adjacent rooms that were visited had stench
possibleWumpus(X, Y) :-
  (certainWumpus(X,Y)  ;   
  (\+visited(r(X,Y)), getAdjacentRooms(r(X,Y),LA), trimNotVisited(LA,LT), (LT = []; checkStenchList(LT)))).
checkStenchList([]).
checkStenchList([H|T]) :- checkStenchList(T), stench(H).

% More easily than checking for pits, as we know there is only one
% Wumpus, one can mix and match adjacent rooms of two or more rooms with
% stench. If only one room that wasnt visited remains, the Wumpus must
% be there.
certainWumpus(X, Y) :-
   (
   setof(R,stench(R),[H|T]), %H is going to be used as reference, and T will help
   getAdjacentRooms(H,LA), %get all adjacent rooms to stench squares
   trimVisited(LA,LAT), %get unvisited rooms adjacent to stench
  %  trimNotAdjacent(LAT,T,LT), %remove those not adjacent to stench
   trimWall(LAT, LW),
   length(LW, 1), %If only one room is reached, that is where the wumpus is
   LW = [r(X,Y)]
   ).

%Returns list of all adjacent rooms
getAdjacentRooms(r(X,Y),L) :-
  XL is X-1,
  XR is X+1,
  YD is Y-1,
  YU is Y+1,
  append([r(XL,Y), r(XR,Y), r(X,YU), r(X,YD)],[],L).

%Checks if one room is adjacent to another room
isAdjacent(r(X,Y),r(XT,YT)) :-
  (X =:= XT, Y =:= YT+1);
  (X =:= XT, Y =:= YT-1);
  (X =:= XT+1, Y =:= YT);
  (X =:= XT-1, Y =:= YT).

%Returns room in front of another in a certain direction
getForwardRoom(r(X0,Y0),D0,r(XN,YN)) :-
  (D0 = north, XN is X0, YN is Y0+1);
  (D0 = east, XN is X0+1, YN is Y0);
  (D0 = south, XN is X0, YN is Y0-1);
  (D0 = west, XN is X0-1, YN is Y0).

trimNotVisited([],[]). %Removes rooms that weren't visited from list of rooms
trimNotVisited([H|T],LT) :- trimNotVisited(T,L), (visited(H) -> append([H],L,LT); LT = L).

trimVisited([],[]). %Removes rooms that were visited from list of rooms
trimVisited([H|T],LT) :- trimVisited(T,L), (visited(H) -> LT = L; append([H],L,LT)).

trimNotAdjacent([],_,[]). %used as trimNotAdjacent(L,T,LT)
trimNotAdjacent(_,[],[]). %Removes rooms from List L that are no adjacent to any room in list T
trimNotAdjacent([LAH|LAT],[TH|TT],LT) :-
    trimNotAdjacent([LAH],TT,LT1),
    trimNotAdjacent(LAT,[TH|TT],LT2),
    append(LT1,LT2,LT3),
    (isAdjacent(LAH,TH) -> append([LAH],LT3,LT) ; LT = LT3).

trimWall([],[]). %Removes rooms that have been confirmed as walls from list of rooms
trimWall([H|T],LT) :- trimWall(T,L), (wall(H) -> LT = L; append([H],L,LT)).