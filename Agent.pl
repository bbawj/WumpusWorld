:- abolish(current/2).
:- abolish(dead_wumpus/1).
:- abolish(actual_wumpus/2).
:- abolish(stench/1).
:- abolish(tingle/1).
:- abolish(glitter/2).
:- abolish(has_gold/1).
:- abolish(shot/1).
:- abolish(visited/1).
:- abolish(is_bump/1).
:- abolish(wall/1).
:- abolish(is_confounded/1).

:- dynamic([
  current/2,
  dead_wumpus/1,
  actual_wumpus/2,
  stench/1,
  tingle/1,
  glitter/2,
  has_gold/1,
  shot/1,
  visited/1,
  is_bump/1,
  wall/1,
  is_confounded/1
]).

% Defines the world NxM matrix.
world(7, 6).
gold(2,3).

% Initial player position
current(r(0, 0), rnorth).
visited(r(0, 0)).

reborn :- 
  retractall(current(_,_)),
  retractall(stench(_)),
  retractall(shot(_)),
  retractall(visited(_)),
  retractall(wall(_)),
  retractall(tingle(_)),
  retractall(glitter(_, _)),
  assertz(visited(r(0,0))),
  assertz(current(r(0,0), rnorth)).

reposition :- 
  retractall(current(_,_)),
  retractall(stench(_)),
  retractall(shot(_)),
  retractall(visited(_)),
  retractall(wall(_)),
  retractall(tingle(_)),
  retractall(glitter(_, _)),
  assertz(current(r(0,0), rnorth)),
  assertz(visited(r(0,0))),
  asserta(is_confounded(yes)).

reposition(L) :- 
  retractall(current(_,_)),
  retractall(stench(_)),
  retractall(shot(_)),
  retractall(visited(_)),
  retractall(wall(_)),
  retractall(tingle(_)),
  retractall(glitter(_, _)),
  assertz(current(r(0,0), rnorth)),
  assertz(visited(r(0,0))),
  asserta(is_confounded(yes)),
  perceptions(L, r(0,0)).

% ---------------------------- %
% Environment predicates       %
% ---------------------------- %
visited(X,Y) :- visited(r(X,Y)).
current(X,Y,D) :- current(r(X,Y),D).
wall(X,Y) :- wall(r(X,Y)).
stench(X,Y) :- stench(r(X,Y)).
tingle(X,Y) :- tingle(r(X,Y)).

hasarrow :- \+shot(yes).

% Perceptions
% ===========
% Process glitter percept into KB
has_glitter(yes, r(X,Y)) :- assertz(glitter(X,Y)), !.
has_glitter(no, _).

% Process tingle percept into KB
has_tingle(yes, Node) :-
  add_tingle_kb(Node).
has_tingle(no, _).

add_tingle_kb(r(X,Y)):-
  \+ tingle(r(X,Y)) -> assertz(tingle(r(X,Y))) ; true.

% Process confounded percept into reposition?
has_confounded(yes) :-
  reposition.
has_confounded(no).
  
% Process stench percept into KB
has_stench(yes, Node) :-
  add_stench_kb(Node).
has_stench(no, _).

add_stench_kb(r(X,Y)):-
  \+ stench(r(X,Y)) -> assertz(stench(r(X,Y))) ; true.

% Add wall to KB if perceive bump
has_bump(yes, Node) :-
  add_wall_kb(Node).
has_bump(no, _).

add_wall_kb(r(X,Y)):-
  \+ wall(r(X,Y)) -> assertz(wall(r(X,Y))) ; true.

% Senses screm if wumpus have died
has_scream(yes) :- assertz(dead_wumpus(yes)), retractall(stench(_)), !.
has_scream(no).

% Returns the current percetions
perceptions([Confounded, Stench, Tingle, Glitter, Bump, Scream], Node) :-
  has_confounded(Confounded), has_stench(Stench, Node), has_tingle(Tingle, Node), has_glitter(Glitter, Node),
  has_bump(Bump, Node), has_scream(Scream), !.

move(A, L) :-
  (
    A = shoot -> shoot(L) ;
    A = moveforward -> moveForward(L)  ;
    A = turnleft -> turnLeft ;
    A = turnright -> turnRight ;
    A = pickup -> pickup(L)
  ).

% Moves the Player to a new position.
moveForward(L) :-
  current(r(X,Y),D),
  getForwardRoom(r(X,Y),D, N),
  perceptions(L, N),
  (
    is_confounded(yes) -> retractall(is_confounded(_));
    \+wall(N) -> (
      retractall(current(_,_)),
      assertz(visited(N)),
      assertz(current(N,D)),
      write("I am at: "), write(N), write(D)) ; false
  ).

turnLeft :- 
  current(r(X,Y),D),
  (D = reast, ND = rnorth, !;
   D = rnorth, ND = rwest, !;
   D = rwest, ND = rsouth, !;
   D = rsouth, ND = reast, !),
  retractall(current(_,_)),
  asserta(current(r(X,Y),ND)).

turnRight :- 
  current(r(X,Y),D),
  (D = reast, ND = rsouth, !;
  D = rsouth, ND = rwest, !;
  D = rwest, ND = rnorth, !;
  D = rnorth, ND = reast, !),
  retractall(current(_,_)),
  asserta(current(r(X,Y),ND)).

pickup(L) :-
  current(r(X,Y), _),
  perceptions(L, r(X,Y)) ,
  glitter(X,Y),
  retract(glitter(X,Y)),
  write("Got the gold!").

% Shoot at given position
shoot(_) :- \+hasarrow, write('I do not have arrows anymore.'), !.
shoot(L) :-
  hasarrow, assertz(shot(yes)),
  current(r(X,Y),_),
  perceptions(L, r(X,Y)).

% Evaluates possibility of Wumpus in a certain room. Checks if all
% adjacent rooms that were visited had stench
wumpus(X, Y) :-
  \+safe(X,Y),
  \+dead_wumpus(yes),
  (
    certainWumpus(X,Y) -> true  ;   
    (\+visited(r(X,Y)), getAdjacentRooms(r(X,Y),LA), trimNotVisited(LA,LT), checkStenchList(LT))
  ),
  (actual_wumpus(X1,Y1) -> (X = X1, Y = Y1) ; true).

checkStenchList([]) :- false, !.
checkStenchList([H|T]) :- \+stench(H) -> checkStenchList(T); true.

% More easily than checking for confunduss, as we know there is only one
% Wumpus, one can mix and match adjacent rooms of two or more rooms with
% stench. If only one room that wasnt visited remains, the Wumpus must
% be there.
certainWumpus(X, Y) :-
   (
   setof(R,stench(R),[H|T]), %H is going to be used as reference, and T will help
   getAdjacentRooms(H,LA), %get all adjacent rooms to stench squares
   trimVisited(LA,LAT), %get unvisited rooms adjacent to stench
   trimWall(LAT, LW),
   trimNotAdjacent(LW, T, LNA),
   length(LNA, 1) ,  %If only one room is reached, that is where the wumpus is
   LNA=[r(X1, Y1)], 
   (\+actual_wumpus(X1, Y1) -> assertz(actual_wumpus(X1, Y1)) ; true),
   LNA = [r(X,Y)]
   ), ! ; 
   (
    getAdjacentRooms(r(X,Y), N),
    trimStench(N, [], NL),
    (length(NL,0) ; length(NL, 1))
    ) -> (\+actual_wumpus(X,Y) -> assertz(actual_wumpus(X,Y)); true) ; false.

trimStench([], L, NL) :- NL = L .
trimStench([H|T], L, NL) :-
  \+stench(H) -> trimStench(T, [H|L], NL); trimStench(T, L, NL).

% Evaluates possibility of confundus in a certain room. Checks if all adjacent
% rooms that were visited had tingles
confundus(X,Y) :- 
  \+safe(X,Y),
  (certainConfundus(X,Y);
  (\+visited(r(X,Y)), getAdjacentRooms(r(X,Y),LA), trimNotVisited(LA,LT), (checkTingleList(LT)))).
checkTingleList([]) :- false.
checkTingleList([H|T]) :- checkTingleList(T) ; tingle(H).

% One can only be certain of a confundus position if there is a room with
% tingle where 3 adjacent rooms were visited and don't have a confundus. The
% pit is in the fourth room certainly.
certainConfundus(X,Y) :-
  getAdjacentRooms(r(X,Y),LA),
  trimNotVisited(LA,LT),
  checkConfundusCertainty(r(X,Y),LT).

checkConfundusCertainty(_,[]) :- false.
checkConfudusCertainty(RP,[H|T]) :-
  tingle(H),
  (
      (
      getAdjacentRooms(H,LA),
      trimVisited(LA,LT),
      trimWall(LT,LT2),
      LT2 = [RP]
      )
      ; checkConfundusCertainty(RP,T)
  ).

% where X,Y are integers, returns true if the Agent knows or can reason that the relative
% position (X,Y) contains neither a Wumpus nor a Confundus Portal.
safe(X,Y) :- safe(r(X,Y)).

safe(r(X,Y)) :- 
  visited(r(X,Y)) -> true ;
  actual_wumpus(X1, Y1) -> (X\=X1, Y\=Y1, getAdjacentRooms(r(X,Y), L), trimNotVisited(L, LT), \+maplist(tingle, LT)) ;
  (getAdjacentRooms(r(X,Y), L), trimNotVisited(L, LT), (\+maplist(stench, LT) , \+maplist(tingle, LT))).

% true if the list L contains a sequence of actions that leads the Agent to inhabit a safe and
% non-visited location.
% explore with a variable will return a dfs path
explore(L) :-
  \+ is_list(L),
  current(r(X,Y), D),
  bfs([[r(X,Y)]], P),
  (P = [] -> (bfsOrigin([[r(X,Y)]], OP), convertPathToMoves(OP, D, [], L) ) ; convertPathToMoves(P, D, [], L)), !.

% explore with a list of nodes will return true if all nodes connected and leads to safe and unvisited node
explore(L) :-
  current(r(X,Y), D),
  ensureActions(L, r(X,Y), D), !.

ensureActions([H|T], CurrentRoom, D) :-
  getRoomFromMove(CurrentRoom, D, H, N),
  getDirectionFromMove(H, D, ND),
  safe(N),
  (length(T, 0) -> \+visited(N); ensureActions(T, N, ND)).

% Helper functions to get first Node from list
getFirstElement([], _).
getFirstElement([H|_], N) :- N = H.

getRoomFromMove(r(X,Y), D, A, N) :-
  XL is X-1,
  XR is X+1,
  YD is Y-1,
  YU is Y+1,
  (
    (A=[turnleft, moveforward], D=rnorth) -> N=r(XL,Y) ;
    (A=[turnleft, moveforward], D=reast) -> N=r(X,YU) ;
    (A=[turnleft, moveforward], D=rwest) -> N=r(X,YD) ;
    (A=[turnleft, moveforward, D=rsouth]) -> N=r(XR,Y) ;
    (A=[turnleft, turnleft, moveforward], D=rnorth) -> N=r(X,YD) ;
    (A=[turnleft, turnleft, moveforward], D=reast) -> N=r(XL, Y) ;
    (A=[turnleft, turnleft, moveforward], D=rwest) -> N=r(XR,Y) ;
    (A=[turnleft, turnleft, moveforward], D=rsouth) -> N=r(X,YU) ;
    (A=[turnright, moveforward], D=rnorth) -> N=r(XR,Y) ;
    (A=[turnright, moveforward], D=reast) -> N=r(X,YD) ;
    (A=[turnright, moveforward], D=rwest) -> N=r(X,YU) ;
    (A=[turnright, moveforward], D=rsouth) -> N=r(XL,Y) ;
    (A=[moveforward], D=rnorth) -> N=r(X,YU) ;
    (A=[moveforward], D=reast) -> N=r(XR,Y) ;
    (A=[moveforward], D=rwest) -> N=r(XL,Y) ;
    (A=[moveforward], D=rsouth) -> N=r(X,YD) ;
    N = r(X,Y)
  ).

consed( A, B, [B|A]).

bfs([], Path) :- Path = [], !.

bfs([[Goal|Visited]|_], Path):-
  safe(Goal), \+visited(Goal), \+wall(Goal), 
  reverse([Goal|Visited], Path), !.

bfs([Visited|Rest], Path) :-                     % take one from front
    Visited = [Start|_],            
    (wall(Start); \+safe(Start)),
    bfs(Rest, Path), !.

bfs([Visited|Rest], Path) :-                     % take one from front
    Visited = [Start|_],            
    safe(Start),
    getAdjacentRooms(Start, L),
    filterRooms(L, Visited, [], Y),
    maplist( consed(Visited), Y, VisitedExtended),      % make many
    append( Rest, VisitedExtended, UpdatedQueue),       % put them at the end
    bfs(UpdatedQueue, Path ).

bfsOrigin([], Path) :- Path = [], !.

bfsOrigin([[Goal|Visited]|_], Path):-
  Goal = r(0,0), 
  reverse([Goal|Visited], Path), !.

bfsOrigin([Visited|Rest], Path) :-                     % take one from front
    Visited = [Start|_],            
    (wall(Start); \+safe(Start)),
    bfsOrigin(Rest, Path), !.

bfsOrigin([Visited|Rest], Path) :-                     % take one from front
    Visited = [Start|_],            
    safe(Start),
    Start \== r(0,0),
    getAdjacentRooms(Start, L),
    filterRooms(L, Visited, [], Y),
    maplist( consed(Visited), Y, VisitedExtended),      % make many
    append( Rest, VisitedExtended, UpdatedQueue),       % put them at the end
    bfsOrigin(UpdatedQueue, Path ).

filterRooms([], _, Final, Sol) :- Sol = Final, !.

filterRooms([H|T], Visited, Final, Sol) :-
  member(H, Visited) -> filterRooms(T, Visited, Final, Sol);
  filterRooms(T, Visited, [H|Final], Sol).

%% Dfs starting from a root
dfs(Root, Path) :-
  dfs([Root], [], Path).
%% dfs(ToVisit, Visited)
%% Done, all visited
dfs([],_, _).
%found a safe unvisited node
dfs([H|_], Visited, Path) :-
  \+member(H, Visited), safe(H), \+visited(H), \+wall(H), append(Visited,[H], UpdatedVisitedList), Path = UpdatedVisitedList, !.
%% Skip elements that are already visited
dfs([H|T],Visited, Path) :-
  (member(H,Visited) ; wall(H); \+safe(H)),
  dfs(T,Visited, Path), !.
%% Add all neigbors of the head to the toVisit
dfs([H|T],Visited, Path) :-
  not(member(H,Visited)),
  safe(H),
  getAdjacentRooms(H, L),
  append(L,T, ToVisit),
  append(Visited, [H], UpdatedVisitedList),
  dfs(ToVisit,UpdatedVisitedList, Path).

convertPathToMoves(L, _, UpdatedMoves, FinalMoves) :-
  length(L, 1),
  FinalMoves = UpdatedMoves, !.

convertPathToMoves([r(X,Y)|T], CurrentDirection, Moves, FinalMoves) :-
  getFirstElement(T, r(X1, Y1)),
  (
    (1 is X1-X, CurrentDirection=rnorth) -> (append(Moves, [[turnright, moveforward]], UpdatedMoves), ND=reast) ;
    (1 is X1-X, CurrentDirection=rsouth) -> (append(Moves, [[turnleft, moveforward]], UpdatedMoves), ND=reast) ;
    (1 is X1-X, CurrentDirection=reast) -> (append(Moves,[[moveforward]], UpdatedMoves) , ND=reast);
    (1 is X1-X, CurrentDirection=rwest) -> (append(Moves,[[turnleft, turnleft, moveforward]], UpdatedMoves), ND=reast) ;
    (1 is X-X1, CurrentDirection=rnorth) -> (append(Moves,[[turnleft, moveforward]], UpdatedMoves), ND=rwest) ;
    (1 is X-X1, CurrentDirection=rsouth) -> (append(Moves,[[turnright, moveforward]], UpdatedMoves), ND=rwest) ;
    (1 is X-X1, CurrentDirection=reast) -> (append(Moves,[[turnleft, turnleft, moveforward]], UpdatedMoves), ND=rwest) ;
    (1 is X-X1, CurrentDirection=rwest) -> (append(Moves,[[moveforward]], UpdatedMoves), ND=rwest);
    (1 is Y-Y1, CurrentDirection=rnorth) -> (append(Moves,[[turnleft, turnleft, moveforward]], UpdatedMoves), ND=rsouth) ;
    (1 is Y-Y1, CurrentDirection=rsouth) -> (append(Moves,[[moveforward]], UpdatedMoves), ND=rsouth) ;
    (1 is Y-Y1, CurrentDirection=reast) -> (append(Moves,[[turnright, moveforward]], UpdatedMoves), ND=rsouth) ;
    (1 is Y-Y1, CurrentDirection=rwest) -> (append(Moves,[[turnleft, moveforward]], UpdatedMoves), ND=rsouth) ;
    (1 is Y1-Y, CurrentDirection=rnorth) -> (append(Moves,[[moveforward]], UpdatedMoves), ND=rnorth) ;
    (1 is Y1-Y, CurrentDirection=rsouth) -> (append(Moves,[[turnleft, turnleft, moveforward]], UpdatedMoves), ND=rnorth) ;
    (1 is Y1-Y, CurrentDirection=reast) -> (append(Moves,[[turnleft, moveforward]], UpdatedMoves), ND=rnorth) ;
    (1 is Y1-Y, CurrentDirection=rwest) -> (append(Moves,[[turnright, moveforward]], UpdatedMoves), ND=rnorth)
  ),
  convertPathToMoves(T, ND, UpdatedMoves, FinalMoves).

getRelativeAdjacentRooms(r(X,Y), D, L) :-
  XL is X-1,
  XR is X+1,
  YD is Y-1,
  YU is Y+1,
  (
    D = rnorth -> append([r(XL,Y), r(XR,Y), r(X,YU), r(X,YD)],[],L) ;
    D = rsouth -> append([r(XR,Y), r(XL,Y), r(X,YD), r(X,YU)],[],L) ;
    D = reast -> append([r(X,YU), r(X,YD), r(XR,Y), r(XL,Y)],[],L) ;
    D = rwest -> append([r(X,YD), r(X,YU), r(XL,Y), r(XR,Y)],[],L)
  ).

getDirectionFromMove(A, D, ND) :-
  (
    (A=[turnleft, moveforward], D=rnorth) -> ND = rwest ;
    (A=[turnleft, moveforward], D=reast) -> ND = rnorth ;
    (A=[turnleft, moveforward], D=rwest) -> ND = rsouth ;
    (A=[turnleft, moveforward], D=rsouth) -> ND = reast ;
    (A=[turnleft, turnleft, moveforward], D=rnorth) -> ND = rsouth ;
    (A=[turnleft, turnleft, moveforward], D=reast) -> ND = rwest ;
    (A=[turnleft, turnleft, moveforward], D=rwest) -> ND = reast ;
    (A=[turnleft, turnleft, moveforward], D=rsouth) -> ND = rnorth ;
    (A=[turnright, moveforward], D=rnorth) -> ND = reast ;
    (A=[turnright, moveforward], D=reast) -> ND = rsouth ;
    (A=[turnright, moveforward], D=rwest) -> ND = rnorth ;
    (A=[turnright, moveforward], D=rsouth) -> ND = rwest ;
    ND = D
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
  (D0 = rnorth, XN is X0, YN is Y0+1), !;
  (D0 = reast, XN is X0+1, YN is Y0), !;
  (D0 = rsouth, XN is X0, YN is Y0-1), !;
  (D0 = rwest, XN is X0-1, YN is Y0), !.

getForwardRoomAndDirection(r(X0,Y0),D0,r(XN,YN, D0)) :-
  (D0 = rnorth, XN is X0, YN is Y0+1), !;
  (D0 = reast, XN is X0+1, YN is Y0), !;
  (D0 = rsouth, XN is X0, YN is Y0-1), !;
  (D0 = rwest, XN is X0-1, YN is Y0), !.

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