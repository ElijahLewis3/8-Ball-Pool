#include "phylib.h"

#include <stdlib.h>
#include <string.h>
#include <math.h>

/********************************
**********  PART  ONE  **********
********************************/

phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos){
    phylib_object *new_still_ball = calloc(1,sizeof(phylib_object));
    if (new_still_ball == NULL){
        return NULL;
    }

    //setting the attributes of the ball (type and number/position)
    new_still_ball->type = PHYLIB_STILL_BALL;
    new_still_ball->obj.still_ball.number = number;
    new_still_ball->obj.still_ball.pos = *pos;

    return new_still_ball;

}

phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc){

    phylib_object *new_rolling_ball = calloc(1,sizeof(phylib_object));
    if (new_rolling_ball == NULL){
        return NULL;
    }

    //setting the attributes of the ball (type, acceleration, number, position, and velocity)
    new_rolling_ball->type = PHYLIB_ROLLING_BALL;
    new_rolling_ball->obj.rolling_ball.acc = *acc;
    new_rolling_ball->obj.rolling_ball.number = number;
    new_rolling_ball->obj.rolling_ball.pos = *pos;
    new_rolling_ball->obj.rolling_ball.vel = *vel;

    return new_rolling_ball;
}

phylib_object *phylib_new_hole(phylib_coord *pos){
    phylib_object *new_hole = calloc(1,sizeof(phylib_object));
    if (new_hole == NULL){
        return NULL;
    }

    //setting the attributes of the hole (position)
    new_hole->type = PHYLIB_HOLE;
    new_hole->obj.hole.pos = *pos;

    return new_hole;
}

phylib_object *phylib_new_hcushion(double y){
    phylib_object *new_hcushion = calloc(1,sizeof(phylib_object));
    if (new_hcushion == NULL){
        return NULL;
    }

    //setting the attributes of the horizontal cushion (position)
    new_hcushion->type = PHYLIB_HCUSHION;
    new_hcushion->obj.hcushion.y = y;

    return new_hcushion;
}

phylib_object *phylib_new_vcushion(double x){
    phylib_object *new_vcushion = calloc(1,sizeof(phylib_object));
    if (new_vcushion == NULL){
        return NULL;
    }

    //setting the attributes of the vertical cushion (position)
    new_vcushion->type = PHYLIB_VCUSHION;
    new_vcushion->obj.vcushion.x = x;

    return new_vcushion;
}


/********************************
************  TABLE  ************
********************************/

phylib_table *phylib_new_table(void){
    phylib_table *new_table = calloc(1,sizeof(phylib_table));
    if (new_table == NULL){
        return NULL;
    }
    new_table->time = 0.0;

    new_table->object[0] = phylib_new_hcushion(0.0);
    new_table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);

    new_table->object[2] = phylib_new_vcushion(0.0);
    new_table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    phylib_coord *topLeft = &(phylib_coord){ .x = 0.0, .y = 0.0 };
    phylib_coord *topRight = &(phylib_coord){ .x = PHYLIB_TABLE_WIDTH, .y = 0.0 };
    phylib_coord *bottomLeft = &(phylib_coord){ .x = 0.0, .y = PHYLIB_TABLE_LENGTH };
    phylib_coord *bottomRight = &(phylib_coord){ .x = PHYLIB_TABLE_WIDTH, .y = PHYLIB_TABLE_LENGTH };
    phylib_coord *middleLeft = &(phylib_coord){ .x = 0.0, .y = (PHYLIB_TABLE_LENGTH/2.0) };
    phylib_coord *middleRight = &(phylib_coord){ .x = PHYLIB_TABLE_WIDTH, .y = (PHYLIB_TABLE_LENGTH/2.0) };


    
    new_table->object[4] = phylib_new_hole(topLeft);
    new_table->object[5] = phylib_new_hole(middleLeft);
    new_table->object[6] = phylib_new_hole(bottomLeft);
    new_table->object[7] = phylib_new_hole(topRight);
    new_table->object[8] = phylib_new_hole(middleRight);
    new_table->object[9] = phylib_new_hole(bottomRight);

    for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++){
        new_table->object[i] = NULL;
    }

    return new_table;
}

/********************************
**********  PART  TWO  **********
********************************/

void phylib_copy_object(phylib_object **dest, phylib_object **src){
    *dest = calloc(1,sizeof(phylib_object));
    
    if (*src != NULL && *dest != NULL){
        memcpy(*dest,*src,sizeof(phylib_object));
    }
    else {
        *dest = NULL;
    }
}


phylib_table *phylib_copy_table(phylib_table *table){
    phylib_table *copy_table = calloc(1,sizeof(phylib_table));
    if (copy_table == NULL){
        return NULL;
    }

    //create a shallow copy of the table
    memcpy(copy_table, table, sizeof(phylib_table));
    copy_table->time = table->time;

    //copy each individual object in the table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if (table->object[i] != NULL){
            // copy_table->object[i] = table->object[i];
            phylib_copy_object(&(copy_table->object[i]),&(table->object[i]));

        }
        else {
            copy_table->object[i] = NULL;
        }
    }
    return copy_table;
}



void phylib_add_object(phylib_table *table, phylib_object *object){
    int i = 0;
    //iterating until it finds something that is  NULL
    while (i < PHYLIB_MAX_OBJECTS){
        if (table->object[i] == NULL){
            table->object[i] = object;
            return;
        }
        i++;
    }
}

void phylib_add_object_index(phylib_table *table, phylib_object *object, int index){
    if (index > -1 && index < 26){
	table->object[index] = object;
    }
}

void phylib_free_table(phylib_table *table){
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if (table->object[i] != NULL){
            free(table->object[i]);
            table->object[i] = NULL;
        }
    }
    free(table);
    table = NULL;
}


phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2){
    phylib_coord sub;

    sub.x = (c1.x - c2.x);
    sub.y = (c1.y - c2.y);
    return sub;
}


double phylib_length(phylib_coord c){
    double xSquare = (c.x * c.x);
    double ySquare = (c.y * c.y);
    double sum = xSquare + ySquare;
    return sqrt(sum);
}


double phylib_dot_product(phylib_coord a, phylib_coord b){
    return ((a.x * b.x) + (a.y * b.y));
}


//obj1 must be a rolling ball, else return -1.0
//if obj2 isn't a valid type return -1.0
double phylib_distance(phylib_object *obj1, phylib_object *obj2) {
    if (obj1 != NULL && obj2 != NULL){
        if (obj1->type != PHYLIB_ROLLING_BALL) {
            return -1.0;
        }
        if (obj2->type != PHYLIB_STILL_BALL &&
            obj2->type != PHYLIB_ROLLING_BALL &&
            obj2->type != PHYLIB_HOLE &&
            obj2->type != PHYLIB_HCUSHION &&
            obj2->type != PHYLIB_VCUSHION) {
            return -1.0;
        }

        double distance;

        // 1) if obj2 is another ball (rolling/still) compute the distance between the center of the 2 balls and subtract two radii
        if (obj2->type == PHYLIB_STILL_BALL){
            phylib_coord stillBall = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos);
            distance = phylib_length(stillBall) - (2.0 * PHYLIB_BALL_RADIUS);

        } 
        else if (obj2->type == PHYLIB_ROLLING_BALL){
            phylib_coord rollingBall = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos);
            distance = phylib_length(rollingBall) - (2.0 * PHYLIB_BALL_RADIUS);
        }

        //2) If obj2 is a HOLE, then compute the distance between the centre of the ball and the hole and subtract the HOLE_RADIUS
        else if (obj2->type == PHYLIB_HOLE) {
            phylib_coord hole = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos);
            distance = phylib_length(hole) - PHYLIB_HOLE_RADIUS;

        } 

        //3) If obj2 is a CUSHION calculate the distance between the centre of the ball and the CUSION and subtract the BALL_RADIUS.
        else if (obj2->type == PHYLIB_HCUSHION) {
            distance = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;

        } 
        else if (obj2->type == PHYLIB_VCUSHION) {
            distance = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;

        }
        else {
            return -1.0;
        }
        return distance;
    }
    return -1.0;
}


/********************************
*********  PART  THREE  *********
********************************/

void phylib_roll(phylib_object *new, phylib_object *old, double time){
    //use new ball function, then copy over values???
    if ((new->type != PHYLIB_ROLLING_BALL) && (old->type != PHYLIB_ROLLING_BALL)){
        return;
    }

    if (new != NULL && old != NULL){

        //formula for position (p = p1 + v1(t) + (0.5 * a1 * (t^2)))
        new->obj.rolling_ball.pos.x = ( (old->obj.rolling_ball.pos.x) + (old->obj.rolling_ball.vel.x * time) + ((old->obj.rolling_ball.acc.x * 0.5) * (time * time)));
        new->obj.rolling_ball.pos.y = ( (old->obj.rolling_ball.pos.y) + (old->obj.rolling_ball.vel.y * time) + ((old->obj.rolling_ball.acc.y * 0.5) * (time * time)));

        //formula for velocity (v = v1 + a1(t))
        new->obj.rolling_ball.vel.x = (old->obj.rolling_ball.vel.x + (old->obj.rolling_ball.acc.x * time));
        new->obj.rolling_ball.vel.y = (old->obj.rolling_ball.vel.y + (old->obj.rolling_ball.acc.y * time));

        //checking if velocity changes signs
        if (old->obj.rolling_ball.vel.x * new->obj.rolling_ball.vel.x < 0){
            new->obj.rolling_ball.vel.x = 0;
            new->obj.rolling_ball.acc.x = 0;
        }
        if (old->obj.rolling_ball.vel.y * new->obj.rolling_ball.vel.y < 0){ 
            new->obj.rolling_ball.vel.y = 0;
            new->obj.rolling_ball.acc.y = 0;
        }
    }
}


unsigned char phylib_stopped(phylib_object *object){
    if (object != NULL && object->type == PHYLIB_ROLLING_BALL && phylib_length(object->obj.rolling_ball.vel) < PHYLIB_VEL_EPSILON){
        unsigned char num = object->obj.rolling_ball.number;
        phylib_coord position = object->obj.rolling_ball.pos;
        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number = num;
        object->obj.still_ball.pos = position;
        return 1;
    }


    return 0;
}

//!TEST THIS FUNCTION
void phylib_bounce(phylib_object **a, phylib_object **b){
    if (*a != NULL && *b != NULL){
        
        unsigned char num = (*b)->obj.rolling_ball.number;
        phylib_coord position = (*b)->obj.rolling_ball.pos;

        switch ((*b)->type)
        {
        case PHYLIB_HCUSHION:
            //negate the y acceleration & velocity
            (*a)->obj.rolling_ball.vel.y *= -1.0;
            (*a)->obj.rolling_ball.acc.y *= -1.0;
            break;

        case PHYLIB_VCUSHION:
            //negate the x acceleration & velocity
            (*a)->obj.rolling_ball.vel.x *= -1.0;
            (*a)->obj.rolling_ball.acc.x *= -1.0;
            break;

        case PHYLIB_HOLE:
            //free the ball
            free(*a);
            *a = NULL;
            break;

        case PHYLIB_STILL_BALL:
            //initialize with 0 acc & vel as well as copy the numbers
            (*b)->type = PHYLIB_ROLLING_BALL;
            (*b)->obj.still_ball.number = num;
            (*b)->obj.still_ball.pos = position;
            
            phylib_coord zeroVel = {0,0};
            phylib_coord zeroAcc = {0,0};
            (*b)->obj.rolling_ball.vel = zeroVel;
            (*b)->obj.rolling_ball.acc = zeroAcc;


            
        case PHYLIB_ROLLING_BALL:
        {
            //relative position of a to b
            phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
            //relative velocity of a to b
            phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

            phylib_coord n;
            n.x = r_ab.x / phylib_length(r_ab);
            n.y = r_ab.y / phylib_length(r_ab);

            double v_rel_n = phylib_dot_product(v_rel,n);

            //Updating velocities
            (*a)->obj.rolling_ball.vel.x -= (v_rel_n * n.x);
            (*a)->obj.rolling_ball.vel.y -= (v_rel_n * n.y);

            (*b)->obj.rolling_ball.vel.x += (v_rel_n * n.x);
            (*b)->obj.rolling_ball.vel.y += (v_rel_n * n.y);

            //Computing speeds
            double speedA = phylib_length((*a)->obj.rolling_ball.vel);
            double speedB = phylib_length((*b)->obj.rolling_ball.vel);

            if (speedA > PHYLIB_VEL_EPSILON){
                (*a)->obj.rolling_ball.acc.x = (-(*a)->obj.rolling_ball.vel.x / speedA) * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = (-(*a)->obj.rolling_ball.vel.y / speedA) * PHYLIB_DRAG;
            } 
            if (speedB > PHYLIB_VEL_EPSILON){
                (*b)->obj.rolling_ball.acc.x = (-(*b)->obj.rolling_ball.vel.x / speedB) * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = (-(*b)->obj.rolling_ball.vel.y / speedB) * PHYLIB_DRAG; 
            }

            break;
        }
        default:
            break;
        }
    }
}

unsigned char phylib_rolling(phylib_table *t){
    int count = 0;
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if (t->object[i] && t->object[i]->type == PHYLIB_ROLLING_BALL){
            count++;
        }
    }
    return count;
}



phylib_table *phylib_segment(phylib_table *table) {
    // no rolling balls
    if (phylib_rolling(table) == 0) {
        return NULL;
    }
    phylib_table *new_table = phylib_copy_table(table);

    double time = PHYLIB_SIM_RATE;

    while (time < PHYLIB_MAX_TIME) {

        //loop over all the objects
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            // if a ball is rolling, apply the roll function to get its new location
            if (new_table->object[i] != NULL && new_table->object[i]->type == PHYLIB_ROLLING_BALL) {
                phylib_roll(new_table->object[i], table->object[i], time);


                //if it stopped before hitting anything, return
                if (phylib_stopped(new_table->object[i])) {
                    new_table->time += time;
                    return new_table;
                }
            }
        }
            
        for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {

            if (new_table->object[j] != NULL && new_table->object[j]->type == PHYLIB_ROLLING_BALL) {
                for (int x = 0; x < PHYLIB_MAX_OBJECTS; x++){

                    //if the distance is less than 0, that means that the object has been hit and the bounce needs to be applied
                    // double distance = phylib_distance(new_table->object[j], new_table->object[x]);
                    if ((phylib_distance(new_table->object[j], new_table->object[x]) < 0.0) && j != x && new_table->object[x] != NULL) {
                        
                        phylib_bounce(&new_table->object[j], &new_table->object[x]);
                        
                        if (new_table->object[x])
                        {
                            phylib_stopped(new_table->object[x]);
                        
                        }
                        new_table->time += time;
                        return new_table;
                    }
                }
            }
        }
            

        // if (time >= PHYLIB_MAX_TIME) {
        //     break;
        // }

        time += PHYLIB_SIM_RATE;
    }

    // new_table->time += time;

    return new_table;
}

char *phylib_object_string( phylib_object *object ){
    static char string[80];
    if (object==NULL){
        snprintf( string, 80, "NULL;" );
        return string;
    }
    switch (object->type){
        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
            "STILL_BALL (%d,%6.1lf,%6.1lf)",
            object->obj.still_ball.number,
            object->obj.still_ball.pos.x,
            object->obj.still_ball.pos.y );
            break;

        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,
            "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
            object->obj.rolling_ball.number,
            object->obj.rolling_ball.pos.x,
            object->obj.rolling_ball.pos.y,
            object->obj.rolling_ball.vel.x,
            object->obj.rolling_ball.vel.y,
            object->obj.rolling_ball.acc.x,
            object->obj.rolling_ball.acc.y );
            break;

        case PHYLIB_HOLE:
            snprintf( string, 80,
            "HOLE (%6.1lf,%6.1lf)",
            object->obj.hole.pos.x,
            object->obj.hole.pos.y );
            break;

        case PHYLIB_HCUSHION:
            snprintf( string, 80,
            "HCUSHION (%6.1lf)",
            object->obj.hcushion.y );
            break;
            
        case PHYLIB_VCUSHION:
            snprintf( string, 80,
            "VCUSHION (%6.1lf)",
            object->obj.vcushion.x );
            break;
    }
    return string;
}
